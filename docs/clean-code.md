### 整洁代码

#### 第2章 有意义的命名
* 名副其实：变量、函数、类名应该已经答复了所有的大问题
* 避免误导：用户组最好用accountGroup而不是accountList
* 不要用前缀：例如属性m_hasChild、接口IShapeFactory
* 类名应该是名词或者名称短语：如WikiPage
* 方法名应该是动词或者动词短语：如DeletePage
* 每个抽象概念选一个词：如fetch、retrieve、get，固定用get

#### 第3章 函数
* 函数的行数不要超过20行
* 每个函数只做一件事
* switch语句的示例，违反了单一原则和开闭原则，当需要增加一个新的Employee类型时，需要修改多处代码
* 零参数函数是最理想的
* 单参数函数常见的两种情况：
  * 需要询问关于那个参数的问题：如bool fileExists("MyFile")
  * 使用改参数修改系统状态：如void includeSetupPage(pageText)
* 双参数函数和三参数函数，除非正好是需要平面坐标或者立体坐标这样的需求
* 函数要么做什么事，要么回答什么事，不可兼得，否则就是做了两件事
* 使用异常替代返回错误码
* 新异常可以从异常类派生出来，这样就无需重新编译

#### 第4章 注释
* 尽量用代码去表达意图而不是注释，因为注释可能没有及时维护
* 像javadoc对每个变量都添加注释的规则是可笑的，只会让代码更加散乱
* 能用代码版本控制表达的，就无需在代码里表达，如注释是代码谁写的
* 注释掉的代码应该直接删除

#### 第5章 格式
* 变量声明：尽可能的靠近其使用位置
* 实体变量：即类属性，应该放在类开头
* 相关函数：a调用b，b调用c，那么a在前，b居中，c在后
* 概念相关：概念相关的代码应该放在一起
* 代码一行最多120个字符

#### 第6章 对象和数据结构
* 对象的定义：充血模型，具有行为的类
* 数据结构的定义：贫血模型，只带属性的类或者只有函数的聚合
* 对象和数据结构的优点：
  * 对象：不需要给对象添加新的行为的前提下，添加新的对象
  * 数据结构：不增加新的对象的前提下，添加新的行为
* 得墨忒耳定律：
  * 模块不应该了解它所操作对象的内部情形
  * 只跟朋友交谈，不和朋友的朋友交谈

#### 第7章 错误
* 使用异常替代返回错误码
* 异常的特点：
  * 错误不可忽略，如果忽略将终止程序
  * happy-path和bad-path容易分离
  * 缺点是破坏了封装性，高层得知道底层可能会抛的异常
* 错误码的特点
  * 缺点1：由于没有约束，如果没有处理可能出现不可预测的情况
  * 缺点2：主流程中充斥着大量检查错误的代码，代码容易混乱
* 别返回null值：如`getEmployees() []Employee`
  * 结果为空不要返回nil，而是空切片，这样就省去了nil判断
* 别传递null值：因为需要nil判断，不然容易出现运行时错误

#### 第8章 边界
* 服务提供者追求普适性，这样能吸引广泛的用户
* 服务使用者则希望满足特定的需求
* 例如想要在只读的map中实现`getSensor(key string) Sensor`
  * 可以直接使用map，但是不能防止其他程序对map进行修改
  * 用一个实体类，对外只提供一个getSensor方法
* 当定义好接口后，对于第三方代码，用适配器模式来包装它

#### 第9章 单元测试
* TDD(Test-Driven-Development)三定律
  * 先写单元测试，再写生产代码
  * 单条单元测试没有通过，则编写它，通过后再写下一条单元测试
  * 单条单元测试没有通过，则编写对应的生产代码，通过后再写下一条单元测试
* FIRST原则
  * fast：测试要能快速运行
  * independent：测试是独立的，能以任何顺序运行，测试之间不应该相互依赖
  * repeatable：可重复测试
  * self-validating：测试结果以布尔值输出，而不需要人工检查输出日志
  * timely：写完生产代码立即编写测试

#### 第10章 类
* 单一职责原则：类应只有一个职责，只有一条修改的理由，应该尽可能的短小(方法不能太多)
* 依赖倒置原则：调用者不再依赖具体类，而是依赖具体类的接口

#### 第11章 系统
* 将构造和使用分离：使用依赖注入
* POJO(Plain Ordinary Java Object)：具有一部分getter/setter方法的那种类就可以称作POJO
* Java Bean：是可复用的组件，具有无参的构造器，还要实现Serializable接口用于实现Bean的持久性

#### 第12章 迭进
* 软件五个设计规则：
  * 运行所有的测试
  * 不可重复
  * 表达了程序员的意图
  * 尽可能的减少类和方法的数量

#### 第13~16章 跳过

#### 第17章 味道和启发
* 何时使用静态方法：它并不在特定对象上操作，操作数来自传参
* 如果不确定是否用静态方法，就用非静态方法































