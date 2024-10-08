### TiDB in Action: 原理和特性

#### 2.讲存储
1. [TiDB 高并发写入场景最佳实践](https://docs.pingcap.com/zh/tidb/stable/high-concurrency-best-practices)
1. [TiDB Best Practice](https://pingcap.com/blog-cn/tidb-best-practice/)
1. [三篇文章了解 TiDB 技术内幕 - 讲存储](https://pingcap.com/blog-cn/tidb-internal-1)
1. Raft 是一个一致性协议，提供几个重要的功能：
  * Leader 选举
  * 成员变更
  * 日志复制
1. 每个数据变更都会落地为一条 Raft 日志，再通过 Raft 的日志来同步副本数据

#### 3.说计算
* [三篇文章了解 TiDB 技术内幕 - 说计算](https://pingcap.com/blog-cn/tidb-internal-2)
* TiDB 最底层用 Raft 来同步数据。每次写入都要写入多数副本，才能对外返回成功。
* 比如最大 3 副本的话，每次写入 2 副本才算成功。写入的延迟取决于最快的两个副本，而不是最慢的那个副本。
* 分布式事务采用的乐观锁。缺点只有在真正提交的时候，才会做冲突检测，所以在冲突严重的场景下性能低下。
* 数据表的数据或者索引具有相同的前缀，这些 Key-Value 会在相邻的位置。批量写入会在很少的几个 Region 上形成写入热点，成为整个系统的瓶颈。
* 二级索引的特点：尽量用区分度比较大的列；最左原则；数据分散在很多Region上，并发查询的Region数可配
* 建议每个事务的行数不超过 200 行，且单行数据小于 100k，否则可能性能不佳。

```
主键索引：key：tableID、rowID；value：\[col1, col2, col3, col4...]
唯一索引：key：tableID、indexID、indexedColumnsValue；value：rowID
非唯一索引：key：tableID、indexID、indexedColumnsValue、rowID；value：null

// 举例有张Age，tableID=10，它的非唯一索引indexID=1，它的唯一索引indexID=2，有三条数据如下
ID Name    Role         Age
1, "TiDB", "SQL Layer", 10
2, "TiKV", "KV Engine", 20
3, "PD",   "Manager",   30

// 主键索引
t10_r1 --> ["TiDB", "SQL Layer", 10]
t10_r2 --> ["TiKV", "KV Engine", 20]
t10_r3 --> ["PD", "Manager", 30]

// 唯一索引[Name]
t10_i2_TiDB --> 1
t10_i2_TiKV --> 2
t10_i2_PB --> 3

// 非唯一索引[Age]
t10_i1_10_1 --> null
t10_i1_20_2 --> null
t10_i1_30_3 --> null
```

#### 4.谈调度
1. [三篇文章了解 TiDB 技术内幕 - 谈调度](https://pingcap.com/blog-cn/tidb-internal-3/)
1. [TiDB 最佳实践系列（二）PD 调度策略最佳实践](https://pingcap.com/blog-cn/best-practice-pd)
1. 相关概念
  * Store：即TiKV实例
  * Region：若Region有3个副本，也即3个Peer。每个Region有1个raft实例，也称Raft Group。
  * Pending / Down：是Peer可能出现的两种特殊状态
    * Pending 表示 Follower 或 Learner 的 raft log 与 Leader 有较大差距，Pending 状态的 Follower 无法被选举成 Leader。
    * Down 是指 Leader 长时间没有收到对应 Peer 的消息，可能是宕机或者网络隔离。
  * Scheduler：是PD的调度器，常用的调度器有：
    * balance-leader-scheduler：保持不同节点的 Leader 均衡。
    * balance-region-scheduler：保持不同节点的 Peer 均衡。
    * hot-region-scheduler：保持不同节点的读写热点 Region 均衡。
    * evict-leader-{store-id}：驱逐某个节点的所有 Leader。（常用于滚动升级）
1. TiKV 节点周期性地向 PD 上报 StoreHeartbeat 和 RegionHeartbeat 两种心跳消息。
1. StoreHeartbeat 包含了 Store 的基本信息，由 Store 定期向 PD 汇报。
  * 总磁盘容量
  * 可用磁盘容量
  * 承载的 Region 数量
  * 数据读写速度
  * 发送/接受的 Snapshot 数量（副本之间可能会通过 Snapshot 同步数据）
  * 是否过载
  * 标签信息
1. RegionHeartbeat 包含了 Region 的相关信息，由 Raft Group 的 Leader 定期向 PD 汇报。
  * Leader 的位置
  * Followers 的位置
  * 掉线副本的个数
  * 数据读写速度

#### 5.TiDB 和 MySQL 的区别
1. MySQL 的时区由环境变量 TZ 或命令行参数 --timezone 决定
1. TiDB 的时区由 TiDB 节点环境变量配置 TZ 决定

#### 6.TiDB 事务模型
1. [6.TiDB 事务模型 · TiDB in Action](https://book.tidb.io/session1/chapter6/tidb-transaction-mode.html)
1. 快照隔离。TiDB 使用 PD 作为全局授时服务（TSO）来提供单调递增的版本号（timestamp）
  * 事务开始时获取 start timestamp
  * 事务提交时获取 commit timestamp，同时也是数据的版本号
  * 事务只能读到在事务 start timestamp 之前的数据（已提交的）
  * 事务在提交时会根据 timestamp 来检测数据冲突
1. TiDB 开始两阶段提交
  * TiDB 向 TiKV 发起 Prewrite 请求。TiKV 检查冲突并加锁。
  * TiDB 收到所有 Prewrite 响应且所有 Prewrite 都成功。
  * TiDB 向 TiKV 发起第二阶段提交。TiKV 执行提交。
  * TiDB 收到所有成功响应则 Success，否则回滚。
1. 乐观锁大事务的缺点：一个事务内包含向10000人转账，过程中有另一个事务向其中一人转账并成功，此大事务提交失败并回滚。
1. 悲观锁性能不如乐观锁：事务内每个 DML 时都需要向 TiKV 发送加锁请求（建议将多条 DML 合并成 一条）
1. 4.0 版本之前对大事务有严格限制，原因有：
  * Prewrite 写下的锁会阻塞其他事务的读，Prewrite 时间长，阻塞的时间也就长。
  * 大事务 Prewrite 时间长，可能会被其他事务终止导致提交失败。

#### 7.TiDB DDL
1. [7.TiDB DDL · TiDB in Action](https://book.tidb.io/session1/chapter7/tidb-ddl-intro.html)
1. 表结构设计最佳实践
  * 设置 SHARD_ROW_ID_BITS 来把 rowID 打散写入多个不同的 Region 中
  * 设置 AUTO_RANDOM 代替 AUTO_INCREMENT 插入数据时自动为整型分配一个随机值
  * 4.0 版本的 PD 会提供 Load Based Splitting 策略，除了根据 Region 的大小进行分裂，还可以根据 QPS。
  * 按日期删除老数据，正常的删除会很慢。如果按日期建立分区表则很快：避免了往TiKV写delete记录，避免了RocksDB的compaction引发的抖动
  * 修改表不允许降低字段长度
  * 不要设计过大的宽表
1. DDL命令：
  * ADMIN SHOW DDL JOBS 5; 显示最近5条DDL命令
  * ADMIN SHOW DDL JOB QUERIES {job_id}; 显示DDL详细信息
  * ADMIN CANCEL DDL JOBS {job_id}; 取消DDL命令
1. DDL 处理流程：
  * 每个 DDL 命令有一个 job_id 并保存在 tikv
  * TiDB 实例会竞选出一个 Owner 节点来执行实际 DDL 任务
  * 两个队列：ADD_INDEX 和非 ADD_INDEX；job_id 小的 DLL 先执行；
1. DDL 变更原理
  * schema 最多有两个版本，版本状态有absent、delete only、write only、public
  * 删除操作如DROP INDEX，DROP TABLE，DROP DATABASE，TRUNCATE TABLE等，先记录到gc_delete_range表，再通过GC机制删除
  * DELETE COLUMN代价比较大，所以只在schema上标记删除
1. [DDL 变更原理](https://book.tidb.io/session1/chapter7/tidb-ddl-status.html)
  * Add column operation：只更新schema，新的row是新结构，查询老的row就依据schema的默认值返回
  * Modify column operation：转换column的类型只支持整型(lengthened)；auto_increment只能在新建表的时候设置；如果索引有用到此column，索引的schema也需改变(但原始数据不变)
  * Add index operation：先生成好index再把index设置为可用，耗时较长
1. Sequence 自增序列
  * CREATE SEQUENCE seq_for_unique START WITH 1 INCREMENT BY 1 CACHE 1000 NOCYCLE; 创建序列
  * SHOW CREATE SEQUENCE seq_for_unique；获取创建序列的SQL
  * DROP SEQUENCE seq_for_unique；删除序列
  * SELECT NEXT/PREVIOUS VALUE FOR seq_for_unique; 获取下一个/上一个自增值
  * CREATE TABLE user ( auto_id int(11) DEFAULT 'nextval(test.seq_for_unique)' ); 表字段使用自增序列
1. AutoRandom 只能用在主键上，不能用在唯一索引

#### 8.Titan 简介与实战
1. [Titan 简介与实战 · TiDB in Action](https://book.tidb.io/session1/chapter8/titan-internal.html)
1. Titan 利用SSD随机IO的优势，以牺牲硬盘空间和范围查询的性能为代价，换取更高的写入性能。
1. Titan 磁盘空间占用可能比 RocksDB 多一倍。
1. Titan 范围查询性能相比 RocksDB 下降 40% 到数倍不等。
1. Titan 适合大value的插入，大于512B即为大value，默认设定是大于1KB。

#### 9.TiFlash 简介与 HTAP 实战
1. [TiFlash 简介与 HTAP 实战 · TiDB in Action](https://book.tidb.io/session1/chapter9/tiflash-intro.html)
1. TiFlash 以Raft Learner的方式接入Multi-Raft组，使用异步的方式同步数据，同时将行格式拆解为列格式
1. TiFlash 的使用：
  * ALTER TABLE tpch50.lineitem SET TIFLASH REPLICA 2; 设置2个TiFlash副本
  * SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA='tpch50' and TABLE_NAME='lineitem'; 查看副本
1. TiFlash 的使用，手工Hint > 会话级别 > Engine级别 > CBO
  * CBO (Cost Based Optimization)：根据优化器来决定是读TiKV还是TiFlash
  * 会话级别：SET SESSION tidb_isolation_read_engines = "tikv,tiflash";
  * Engine级别，实例配置：isolation-read.engines = ["tikv", "tiflash"]
  * 手工Hint：SELECT /*+ read_from_storage(tiflash[t]) */ * FROM t;

#### 10.TiDB 安全
1. 权限管理
  * 创建用户：CREATE USER 'developer'@'192.168.0.%' IDENTIFIED BY 'password';
  * 授权用户：GRANT SELECT ON db1.table1 TO 'developer'@'192.168.0.%';
  * 修改密码：ALTER USER 'developer'@'192.168.0.%' IDENTIFIED BY 'password';
1. RBAC
  * 创建角色：create role reader@'%';
  * 授权角色：grant select on db1.table1 to reader'%';
  * 角色给用户：grant reader to developer'192.168.0.%';
  * 连接后：set role reader; 使角色生效
1. 证书管理与数据加密
  * 证书来确认身份，登陆后使用加密连接来传输数据。越来越多的用户使用证书鉴权来代替用户名密码验证。
  * 用户需要生成：服务端密钥和证书，客户端密钥和证书。再用CA密钥和证书对服务端证书和客户端证书进行签名。
  * 生成CA密钥和证书：ca-key.pem、ca-cert.pem
  * 生成服务器密钥和证书：server-key.pem、server-cert.pem(CA密钥和证书)
  * 生成客户端密钥和证书：client-key.pem、client-cert.pem(CA密钥和证书)
  * 验证证书是否正确：openssl verify -CAfile ca-cert.pem server-cert.pem client-cert.pem
  * 服务器需要存放CA证书、服务端密钥和证书
  * 客户端需要存放CA证书、客户端密钥和证书
  * CA密钥则需要离线保管

#### TiSpark 的简介和实战
1. [Spark架构与原理这一篇就够了](https://www.cnblogs.com/skaarl/p/13960639.html)
1. Hadoop和Spark的区别
  * Spark 是为了跟 Hadoop 配合而开发出来的，不是为了取代 Hadoop
  * Hadoop 一次 MapReduce 之后结果写入磁盘中，二次 MapReduce 时从磁盘读取，瓶颈在2次运算多余的 IO 消耗
  * Spark 则是将数据一直缓存在内存中直到计算得到最后的结果，再写入磁盘
1. Hadoop 集群的 Hive 表廉价，稳定且成熟，不适合存放频繁变化的数据。