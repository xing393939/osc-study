### AWS认证英语学习

#### Chapter 2 Amazon Elastic Compute Cloud and Amazon Elastic Block Store
```
Tenancy

To meet special regulatory requirements, your organization’s instances might need an 
extra level of isolation. The Dedicated Instance option ensures that your instance will run 
on a dedicated physical server. This means that it won’t be sharing the server with resources
owned by a different customer account. The Dedicated Host option allows you to actually 
identify and control the physical server you’ve been assigned to meet more restrictive 
licensing or regulatory requirements.

dedicated
美[ˈdedɪkeɪtɪd]
adj. 专用的

restrictive
美[rɪˈstrɪktɪv]
adj. 限制的

tenancy
美[ˈtɛnənsi]
n. 租用
```

```
Resource Tags

The more resources you deploy on your AWS account, the harder it can be to properly keep 
track of things. Having constantly changing numbers of EC2 instances—along with accompanying 
storage volumes, security groups, and elastic IP addresses—all spread across two 
or three VPCs can get complicated.

constantly
美[ˈkɑːnstəntli]
adv. 时常地

accompanying
美[ə'kʌmpənɪɪŋ]
adj. 陪伴的

complicated
美[ˈkɑːmplɪkeɪtɪd]
adj. 复杂的
```

```
NAT Devices

One solution is to use network address translation (NAT) to give your private instance 
access to the Internet without allowing access to it from the Internet. AWS gives you two 
ways to do that: a NAT instance and a NAT gateway (see Figure 2.2). They’ll both do the 
job, but since a NAT gateway is a managed service, it doesn’t require that you manually 
launch and maintain an instance. Both approaches will incur monthly charges.

NAT Gateway 是VPC共享的，AZ1和AZ2都能用，只需建一个，如果考虑容灾可以每个AZ都建一个。

approach
美[əˈproʊtʃ]
n. 方法

charge
美[tʃɑːrdʒ]
n. 收费
```

```
Health Checks Against Application Instances

A good design practice is to have a few recovery actions that work for a 
variety of circumstances. An instance may crash due to an out-of-memory 
condition, a bug, a deleted file, or an isolated network failure, but simply 
terminating and replacing the instance using Auto Scaling resolves all these 
cases. There’s no need to come up with a separate recovery action for each 
cause when simply re-creating the instance solves them all.

variety
美[vəˈraɪəti]
n. 多种多样

circumstance
美[ˈsɜːrkəmstæns]
n. 条件；环境

separate
美[ˈsepəreɪt]
adj. 独立的
```

```
Summary

EC2 Auto Scaling can help you avoid application failures caused by overloaded 
instances. By implementing dynamic scaling policies, you can ensure that you always have 
enough instances to handle increased demand. In the event of some failure, a well-designed 
Auto Scaling group will ensure that you always have a minimum number of healthy 
instances. When an instance becomes unhealthy, Auto Scaling will terminate and replace it.
```

#### Chapter 3 AWS Storage

```
Introduction

In this chapter, you’re going to learn the following:
■ How S3 objects are saved, managed, and accessed
■ How to choose from among the various classes of storage to get the right balance of 
durability, availability, and cost
■ How to manage long-term data storage lifecycles by incorporating Amazon Glacier 
into your design
■ What other AWS services exist to help you with your data storage and access 
operations

durability
美[ˌdjʊrəˈbɪlətɪ]
n. 持久性

incorporate
美[ɪnˈkɔːrpəreɪt]
vt. 使混合
```

```
Eventually Consistent Data

It’s important to bear in mind that S3 replicates data across multiple locations. As a result, 
there might be brief delays while updates to existing objects propagate across the system. 
Uploading a new version of a file or, alternatively, deleting an old file altogether can result 
in one site reflecting the new state with another still unaware of any changes.

To ensure that there’s never a conflict between versions of a single object—which could 
lead to serious data and application corruption—you should treat your data according to 
an eventually consistent standard. That is, you should expect a delay (usually just two seconds 
or less) and design your operations accordingly.

Because there isn’t the risk of corruption when creating new objects, S3 provides read-after-write 
consistency for creation (PUT) operations. （针对new object，把请求发给固定的副本，保证客户端写后能立马读到它。）

bear
美[ber]
v. 带有，拥有

replicate
美[ˈreplɪkeɪt]
vt. 复制

brief
美[briːf]
adj. 短暂的

propagate
美[ˈprɑːpəɡeɪt]
vt. 扩散；使蔓延

reflect
美[rɪˈflekt]
v. 反映；反射

conflict
英[ˈkɒnflɪkt]
n. 争执；冲突

serious
美[ˈsɪriəs]
adj. 严重的

corruption
美[kəˈrʌpʃn]
n. 腐败

accordingly
美[əˈkɔːrdɪŋli]
adv. 相应地
```

```
Accessing S3 Objects

There is more than a little overlap between those three approaches. In fact, ACLs are 
really leftovers from before AWS created IAM. As a rule, Amazon recommends applying S3 
bucket policies or IAM policies instead of ACLs.

overlap
英[ˌəʊvəˈlæp]
vt. 重叠

approach
美[əˈproʊtʃ]
n. 方法
```

```
Summary

You can reduce the size and cost of your requests against S3 and Glacier-based data by 
leveraging the SQL-like Select feature. You can also provide inexpensive and simple static 
websites through S3 buckets.

Amazon Glacier stores your data archives in vaults that might require hours to retrieve 
but that cost considerably less than the S3 storage classes.

leverage
美[ˈlevərɪdʒ]
v. 发挥杠杆作用；利用
```

#### Chapter 4 Amazon Virtual Private Cloud

```
Introduction

If you’re familiar with the components of a traditional network, you’ll recognize many 
VPC components. But although VPCs function like a traditional TCP/IP network, they are 
scalable, allowing you to expand and extend your network without having to add physical 
hardware. To make this scalability possible, some components that you’d find in a 
traditional network—such as routers, switches, and VLANs—don’t exist in VPCs. Instead, 
they’re abstracted into software functions and called by different names.

traditional
美[trəˈdɪʃənl]
adj. 传统的

recognize
美[ˈrekəɡnaɪz]
vt. 认出

scalable
美['skeɪləbəl]
adj. 可攀登的，可升级的
```

```
Subnet CIDR Blocks

A subnet can’t have multiple CIDRs. Unlike a VPC that can have secondary CIDRs, a 
subnet can have only one. However, if a VPC has a primary CIDR and a secondary CIDR, 
your subnet’s CIDR can be derived from either. For example, if your VPC has the primary 
CIDR of 172.16.0.0/16 and a secondary CIDR of 172.17.0.0/16, a subnet in that VPC 
could be 172.17.12.0/24, as it’s derived from the secondary VPC CIDR.

derive
美[dɪˈraɪv]
v. 获得
```

```
Using Network Access Control Lists and Security Groups Together

You may want to use an NACL in addition to a security group so that you aren’t dependent 
on AWS administrators to specify the correct security group when they launch an instance. 
Because an NACL is applied to the subnet, the rules of the NACL apply to all traffic 
ingressing and egressing the subnet, regardless of how the security groups are configured.

regardless
美[rɪˈɡɑːrdləs]
adv. 不顾后果地
```

```
NAT Instance

One advantage of a NAT instance is that you can use it as a bastion host, sometimes 
called a jump host, to connect to instances that don’t have a public IP. You can’t do this 
with a NAT gateway.

You must create a default route to direct Internet-bound traffic to the NAT instance. 
The target of the default route will be the NAT instance’s ID, which follows the format 
i-0a1674fe5671dcb00.

advantage
美[ədˈvæntɪdʒ]
n. 优点

bastion
美[ˈbæstʃən]
n. 堡垒
```

```
Hybrid Cloud Networking

1. Site to Site VPN (Internet Protocol security, IPsec)
2. AWS Transit Gateway
3. AWS Direct Connect (DX)

However, if you want to connect a large number of VPCs to your on-premises network, 
or if you need to connect many on-premises networks to a VPC, creating a separate VPN 
connection for each one can become cumbersome. In that case, you’ll want to use AWS 
Transit Gateway

Hybrid
美[ˈhaɪbrɪd]
adj. 混合

on-premises
内部部署的

transit
美[ˈtrænzɪt]
adj. 中转的
```

```
Summary

In each region, AWS automatically provides a default VPC with default subnets, a main 
route table, a default security group, and a default NACL. Many use a default VPC for a 
long time without ever having to configure a VPC from scratch. This makes it all the more 
important that you as an AWS architect understand how to configure a virtual network 
infrastructure from scratch. There’s a good chance you won’t be allowed to modify an 
infrastructure that was built on top of a default VPC. Instead, you may be tasked with 
replicating it from the ground up—troubleshooting various issues along the way. Practice what 
you’ve learned in this chapter until creating fully functional VPCs becomes second nature 
to you.

infrastructure
美[ˈɪnfrəstrʌktʃər]
n. 基础设施
```

#### Chapter 5 Database Services

```
General-Purpose SSD
Burst duration in seconds = Credit balance / 3000 - 3 * (size in GB)
如果有200GB的gp2磁盘，基准可达到600IOPS，Credit balance上限是5400000
如果Credit balance为0，每秒可以积累600个
如果Credit balance为5400000，要突发到3000IOPS，可以持续2250秒

Provisioned IOPS SSD (io1)
The ratio of storage in gigabytes to IOPS must be at least 50:1. For example, if you want 32,000 IOPS, 
you must provision at least 640 GB of storage.

The st1 and sc1 volume types are appropriate for frequent, sequential reads 
and writes, such as you might see with data warehousing, extract, transform, 
and load (ETL), and Elastic MapReduce (EMR) applications. These 
volume types are not appropriate for random I/O. For that, gp2 is a better 
choice.

Both RDS MySQL and Aurora MySQL support Cross-Region.
Aurora MySQL support maximum of 4 instances in a multi-master cluster, can't enable cross-Region replicas.
IAM authentication isn’t supported for MS-SQL, Oracle.
Multi-region failover, isn’t supported for MS-SQL, PostgreSQL, or Oracle.
Multi-region failover, standby instance is not a read replica and cannot serve read traffic. When a failover occurs, RDS changes the DNS record of the endpoint to point to the standby.
Point-in-time recovery for RDS, should enable automatic backups, recovery to fixed backup snapshot.
Point-in-time recovery for Aurora, recovery to any time with-in the backup retention period.
```

```
DynamoDB
https://www.modb.pro/db/65288
https://stackoverflow.com/questions/56051481

表有三种索引：
Table Primary Key（必须）
Global Secondary Index（可选，可以选择任意属性作为HashKey和RangeKey）
Local Secondary Index（可选，只能选择与表相同的HashKey，创建表时指定，和表共享吞吐量，最大10G）

索引的两种组成类型：
只包含HashKey：HashKey又称为分区键
包含HashKey+RangeKey组合，RangeKey也称排序键

HashKey、RangeKey的类型只能是String、Number、Binary

DynamoDB的where查询超过2个字段，则建一个冗余的联合字段，然后设置Global Secondary Index或Local Secondary Index
```

```
DynamoDB Global Tables 

To use global tables, your table must be configured in on-demand mode or provisioned 
mode with Auto Scaling enabled. A global table is a collection of replica tables, and 
a global table can have only one replica table per region. Whenever you write an item to a 
replica table, it’s replicated to replica tables in other regions. Global tables don’t support 
strongly consistent read across regions.
```

```
Summary

Whether you implement a relational or nonrelational database depends solely on the 
application that will use it. Relational databases have been around a long time, and many 
application developers default to modeling their data to fit into a relational database. Applications 
use database-specific SDKs to interact with the database, so often the needs of the 
application mandate the specific database engine required. This is why AWS RDS offers six 
of the most popular database engines and sports compatibility with a wide range of versions. 
The idea is to let you take an existing database and port it to RDS without having to 
make any changes to the application.

solely
美[ˈsoʊlli]
adv. 唯一地

mandate
美[ˈmændeɪt]
vt. 托管；批准
```

#### Chapter 6 Authentication and Authorization—AWS Identity and Access Management

```
User and Root Accounts

You may be forgiven for wondering why giving a user the AdministratorAccess 
policy is any safer than leaving your root account in active service. 
After all, both seem to have complete control over all your resources, right? 
Wrong. There are some powers that even an AdministratorAccess holder 
doesn’t have, including the ability to create or delete account-wide budgets 
and enable MFA Delete on an S3 bucket.
```

```
Roles

You create a new role by defining the trusted entity you want given access. There are 
four categories of trusted entity: an AWS service; another AWS account (identified by its 
account ID); a web identity who authenticates using a login with Amazon, Amazon Cognito, 
Facebook, or Google; and Security Assertion Markup Language (SAML) 2.0 federation with 
a SAML provider you define separately.

Once your entity is defined, you give it permissions by creating and attaching your own 
policy document or assigning one or more preset IAM policies. When a trusted entity 
assumes its new role, AWS issues it a time-limited security token using the AWS Security 
Token Service (STS).

authenticate
英[ɔ:ˈθentɪkeɪt]
vt. 证明是真实的

federation
美[ˌfedəˈreɪʃn]
n. 联邦

assume
美[əˈsuːm]
v. 假设
```

```
Authentication Tools

登录协议有（https://zhuanlan.zhihu.com/p/105674989）：
LDAP：角色有用户、应用Server、LADP server。LADP server只负责认证登录。
SAML 2.0：角色有用户、应用Server、LDP server。LDP server负责登录认证和授权。
OAuth 2.0：角色有用户、应用Server、第三方Server。第三方Server负责登录认证和授权。
OpenID：角色有用户、应用Server、用户的LDP Server。用户的LDP Server只负责认证登录。

Handling user authentication
1. Amazon Cognito
2. AWS Managed Microsoft AD
3. AWS Single Sign-On

Administration of encryption keys and authentication secrets
1. AWS Key Management Service (KMS)。CMK 仅仅支持导入对称密钥，不支持非对称密钥。
2. AWS Secrets Manager
3. AWS CloudHSM

代码保存db password的方法有：
1. 使用AWS Secrets Manager
2. 使用AWS Systen Manager的Parameter Store，可存明文或者KMS加密的密文，免费
3. 使用AWS Systen Manager的AppConfig
```

```
Summary

The IAM root user that’s automatically enabled on a new AWS account should ideally be 
locked down and not used for day-to-day account operations. Instead, you should give 
individual users the precise permissions they’ll need to perform their jobs.

All user accounts should be protected by strong passwords, multifactor authentication, 
and the use of encryption certificates and access keys for resource access.

Once authenticated, a user can be authorized to access a defined set of AWS resources 
using IAM policies. It’s a good practice to associate users with overlapping access needs 
into IAM groups, where their permissions can be centrally and easily updated. Users can 
also be assigned temporary IAM roles to give them the access they need, when they need it.
Access keys should be regularly audited to ensure that unused keys are deleted and active 
keys are rotated at set intervals.

Identities (including users, groups, and roles) can be authenticated using a number of 
AWS services, including Cognito, Managed Microsoft AD, and Single Sign-On. Authentication 
secrets are managed by services such as AWS Key Management Service (KMS), AWS 
Secrets Manager, and AWS CloudHSM.

precise
美[prɪˈsaɪs]
adj. 清晰的

associate
英[əˈsəʊʃieɪt]
v. 使与有关系
```

#### Chapter 7 CloudTrail, CloudWatch, and AWS Config

```
Introduction

CloudTrail, CloudWatch, and AWS Config are three services that can help you ensure the 
health, performance, and security of your AWS resources and applications. These services 
collectively help you keep an eye on your AWS environment by performing the following 
operational tasks:
1. Tracking Performance
2. Detecting Application Problems
3. Detecting Security Problems 
4. Logging Events 
5. Maintaining an Inventory of AWS Resources 

CloudWatch does not automatically provide memory and disk utilization metrics of your instances.

trail
美[treɪl]
n. 踪迹

detect
美[dɪˈtekt]
v. 发现；查明

inventory
美[ˈɪnvəntɔːri]
n. 存货清单；财产目录
```

```
Metric Filters

You would create a metric filter to track the number of times the string “404” appears in the HTTP 
status code section of the log. Every time CloudWatch Logs receives a log event that matches the filter, 
it increments a custom metric. You might name such a metric HTTP404Errors and store it in the custom 
Apache namespace.
```

```
CloudWatch Alarms - Threshold

Static Threshold. You define a static threshold by specifying a value and a condition. 
If you want to trigger an alarm when CPUUtilization meets or exceeds 50 percent, 
you would set the threshold for that alarm to >= 50. Or if you want to know when 
CPUCreditBalance falls below 800, you would set the threshold to < 800.

Anomaly Detection. Anomaly detection is based on whether a metric falls outside of 
a range of values called a band. You define the size of the band based on the number 
of standard deviations. For example, if you set an anomaly detection threshold of 2, 
the alarm would trigger when a value is outside of two standard deviations from the
average of the values.

threshold
美[ˈθreʃhoʊld]
n. 门槛

anomaly
美[əˈnɑməli]
n. 异常
```

```
CloudWatch Alarms - Alarm States

As an example, if the period is five minutes and the data points to alarm is 3, then the  
data points to monitor must cross and remain crossing the threshold for 15 minutes before the 
alarm goes into an ALARM state.
```

```
CloudWatch Alarms - Data Points to Alarm and Evaluation Period

To give an illustration, let’s say you create an alarm with a threshold of >= 40. The 
data points to alarm is 2, and the evaluation period is 3, so this is a 2 out of 3 alarm. Now 
suppose CloudWatch evaluates the following three consecutive data points: 46, 39, and 
41. Two of the three data points exceed the threshold, so the alarm will transition to the 
ALARM state.

Following that, CloudWatch evaluates the consecutive data points 45, 30, and 25. Two 
of the three data points fall below the threshold, so the alarm transitions to an OK state. 
Notice that CloudWatch must evaluate three data points (the evaluation period) before it 
changes the alarm state.

evaluation
美[ɪˌvæljuˈeɪʃn]
n. 评估

transition
美[trænˈzɪʃn]
v. 转变，过渡
```

```
Amazon EventBridge (CloudWatch Events)

For example, a running EC2 instance entering the stopped state would be an event. An IAM user 
logging into the AWS Management Console would be another event. EventBridge can automatically take 
immediate action in response to such events.
```

```
Summary

You must configure CloudWatch and AWS Config before they can begin monitoring your 
resources. CloudTrail automatically logs only the last 90 days of management events even if 
you don’t configure it. It’s therefore a good idea to configure these services early on in your 
AWS deployment.

CloudWatch, CloudTrail, and AWS Config serve different purposes, and it’s important 
to know the differences among them and when each is appropriate for a given use case.
CloudWatch tracks performance metrics and can take some action in response to those 
metrics. It can also collect and consolidate logs from multiple sources for storage and 
searching, as well as extract metrics from them.

CloudTrail keeps a detailed record of activities performed on your AWS account for 
security or auditing purposes. You can choose to log read-only or write-only management 
or data events.

AWS Config records resource configurations and relationships past, present, and future. 
You can look back in time to see how a resource was configured at any point. AWS Config 
can also compare current resource configurations against rules to ensure that you’re in 
compliance with whatever baseline you define.

consolidate
美[kənˈsɑːlɪdeɪt]
v. 合并

compliance
美[kəmˈplaɪəns]
n. 遵守
```

#### Chapter 8 The Domain Name System and Network Routing: Amazon Route 53 and Amazon CloudFront

```
Routing Policies

1. Simple is the default routing policy for new record sets.
2. Weighted Routing 
3. Latency Routing. Base on your resources running in multiple AWS regions
4. Failover Routing. Set to redirect traffic to a backup resource when primary resource is offline
5. Geolocation Routing. Restrict content to regions where it’s legally permitted
6. Multivalue Answer Routing. 每个A记录对应一个ip和一个healthCheck, failover就剔除，类似ALB
```

```
Summary

Weighted routing policies let you direct traffic among multiple parallel resources proportionally according to their ability to handle it. Latency routing policies send traffic to 
multiple resources to provide the lowest-latency service possible. Failover routing monitors a resource and, on failure, reroutes subsequent traffic to a backup resource. Geolocation routing assesses the location of a request source and directs responses to appropriate 
resources.

Amazon CloudFront is a CDN that caches content at edge locations to provide lowlatency delivery of websites and digital media.

parallel
美[ˈpærəlel]
adj. 并行的

subsequent
美[ˈsʌbsɪkwənt]
adj. 随后的

appropriate
美[əˈproʊprieɪt]
adj. 适当的

edge
美[edʒ]
n. 边线；刀锋
```

#### Chapter 9 Simple Queue Service and Kinesis

```
Kinesis Data Firehose vs. Kinesis Data Streams

Kinesis Data Firehose, on the other hand, is not an open-ended producer-consumer 
model where a consumer can simply subscribe to a stream. Instead, you must specify one or 
more destinations for the data.

Kinesis Data Firehose is tightly integrated with managed AWS services and third-party 
applications, so it’s generally more appropriate for streaming data to services such
as Redshift, S3, or Splunk. Kinesis Data Streams, on the other hand, is usually the better 
choice for streaming data to a custom application. Refer to Table 9.1 for a comparison of 
SQS and Kinesis services.

open-ended
美[ˈopənˈɛndɪd]
adj. 广泛的，无限度的

specify
美[ˈspesɪfaɪ]
vt. 指定

tightly
美[ˈtaɪtli]
adv. 紧紧地

integrated
美[ˈɪntɪɡreɪtɪd]
adj. 结合的
```

```
Summary

SQS acts as a highly available buffer for data that must move between different application 
components. On the other hand, the Kinesis services collect, process, and store streaming, 
real-time binary data such as audio and video. Both SQS and the Kinesis services enable 
loose coupling.

loose
美[luːs]
adj. 松散的

coupling
美[ˈkʌplɪŋ]
n. 耦合
```












