### TiDB in Action: 部署与管理

#### 1.部署安装和常见运维
1. TiUP 命令
  * 升级TiUP：tiup update --self 
  * 扩容：配置scale.yaml填上要扩容的节点ip和端口，执行tiup cluster scale-out tidb-test scale.yaml
  * 缩容：tiup cluster scale-in prod-cluster -N 172.16.5.140:20160
1. 升级 PD：优先升级非 Leader 节点；再将 Leader 迁移到升级完成的节点上；再升级旧的 Leader 节点
1. 升级 TiKV：
  * 先在 PD 中添加一个迁移对应 TiKV 上 region leader 的调度
  * 再对该 TiKV 节点进行升级更新
  * 等更新后的 TiKV 正常启动之后再移除迁移 Leader 的调度

#### 备份恢复和导入导出
1. 增量数据订阅工具 CDC
  * 工作原理：TiKV 负责拼装 KV 变更日志（Change Logs），并输出到 TiCDC 集群。
1. 数据导入工具 Lightning
1. 分布式备份和恢复工具 BR
1. 数据导出工具 Dumpling


