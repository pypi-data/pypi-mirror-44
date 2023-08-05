# 介绍

常用工具整理

* 统一的 JSON 日志输出方式的 Logger
* 环境变量、zk 配置读取 (需要 kazoo 库)
* 通过服务名称获取服务地址 (需要 requests 库)
* 服务告警 (需要 requests 库)
* 生成业务流水号
* rabbit MQ 消息推送 (需要 pika)
* kafka 消息推送 (需要 kafka-python)

# 日志

``` python
from jkutils.logger import JKLogger

logger = JKLogger("jk_utils")

logger.debug("debug")
logger.info("info")
# 设置默认字段，后面的log都会带上默认字段
logger.set_default_fields(log_id=logger.log_id, default_id="000000000")
logger.warning("warning")
logger.warn("warn")
logger.error("error")
# 移除默认字段 可以传任意个 key
logger.remove_default_field("default_id", "test_id")
logger.critical("critical")
# 带上额外字段
logger.info("dict", uid=123, phone="12774147414")
# 移除所有默认字段
logger.remove_default_all_fields()
logging.info("logging info")

```

在 **flask** 中使用时，如果你设置的默认字段生命周期只在同一次请求时，请在创建对象时设置 `default_fileds_obj` 为：

``` python
from jkutils.logger import JKLogger, FlaskGStorage
logger = JKLogger("jk_utils", default_fileds_obj=FlaskGStorage())

```

在 **多线程** 中使用时，如果你设置的默认字段生命周期只在同一线程内时，请在创建对象时设置 `default_fileds_obj` 为：

``` python
from jkutils.logger import JKLogger, ThreadLocalStorage
logger = JKLogger("jk_utils", default_fileds_obj=ThreadLocalStorage())

```

结果类似

``` json
{"msg": "info", "funcname": "test_log", "file": "/home/jianshijiuyou/python_code/xwjk-base/tests/test_log.py:12", "level": "INFO", "project": "jk_utils", "time": "2019-03-03 11:26:37"}
{"log_id": "48c1fc3068d748fa9b100f68d679cf3e", "default_id": "000000000", "msg": "warning", "funcname": "test_log", "file": "/home/jianshijiuyou/python_code/xwjk-base/tests/test_log.py:14", "level": "WARNING", "project": "jk_utils", "time": "2019-03-03 11:26:37"}
{"log_id": "48c1fc3068d748fa9b100f68d679cf3e", "default_id": "000000000", "msg": "warn", "funcname": "test_log", "file": "/home/jianshijiuyou/python_code/xwjk-base/tests/test_log.py:15", "level": "WARNING", "project": "jk_utils", "time": "2019-03-03 11:26:37"}
{"log_id": "48c1fc3068d748fa9b100f68d679cf3e", "default_id": "000000000", "msg": "error", "funcname": "test_log", "file": "/home/jianshijiuyou/python_code/xwjk-base/tests/test_log.py:16", "level": "ERROR", "project": "jk_utils", "time": "2019-03-03 11:26:37"}
{"log_id": "48c1fc3068d748fa9b100f68d679cf3e", "msg": "critical", "funcname": "test_log", "file": "/home/jianshijiuyou/python_code/xwjk-base/tests/test_log.py:18", "level": "CRITICAL", "project": "jk_utils", "time": "2019-03-03 11:26:37"}
{"uid": 123, "phone": "12774147414", "log_id": "48c1fc3068d748fa9b100f68d679cf3e", "msg": "dict", "funcname": "test_log", "file": "/home/jianshijiuyou/python_code/xwjk-base/tests/test_log.py:19", "level": "INFO", "project": "jk_utils", "time": "2019-03-03 11:26:37"}
{"msg": "logging info", "funcname": "test_log", "file": "/home/jianshijiuyou/python_code/xwjk-base/tests/test_log.py:21", "level": "INFO", "project": "jk_utils", "time": "2019-03-03 11:26:37"}
```

注意原生 `logging` 也被修改了的，如果不需要

``` python
logger = JKLogger("jk_utils", native=False)
```

设置日志级别、时间格式

``` python
logger = JKLogger("jk_utils", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S", native=True)

```

# 读取环境变量/zk

``` python
from jkutils.env import EnvZk

ez = EnvZk("111.230.231.xx:port,111.230.231.xx:port,111.230.231.xx:port", "server_name", "服务注册地址")

CUR_ENV = ez.init_conf("CUR_ENV", force=True)
CHAOS_DB = ez.init_conf("test_bool",default="true", conftype=bool, force=False)

# init_conf 的签名为
# def init_conf(self, name, default=None, conftype=None,
#               force=False, hash_log=None):


```

以上是初始化获取参数的方式

还可以动态获取参数，但是动态获取的参数必须是之前初始化过的

``` python
report_exc_url =  ez["REPORT_EXC_URL"]
```

参数读取顺序为

```
读取顺序: 环境变量 > zk > default
```

## 监听配置变化

``` python
def test(config):
    print(config)

ez = EnvZk(...)
ez.add_listener(test)
# 添加多个监听器请设置 key
ez.add_listener(test, key="other")
# 删除监听器只需要将对应 key 的 func 设置为 None
ez.add_listener(None)
# or
ez.add_listener(None, key="other")
```

# 获取服务地址

``` python
from jkutils.get_host_ip import get_host_ip

chaos_host = get_host_ip(url, "chaos")

```

# 服务告警

``` python
from jkutils.report_exception import AbnormalReport

ar = AbnormalReport("chaos", "bank", report_url)
# 设置告警级别 code
ar.set_err_code(1001, 1002, 1003)

# 告警
ar.report("title", "出 bug 啦～～～")
```

支持参数

``` python
AbnormalReport(project_name, env_flag, url=None, timeout=15):

report(self, title, content, cid=AbnormalReport.GENERAL_ERROR):
```

# 获取当前 git commit id（如果存在）

``` python
from jkutils.git import git_revision_hash
commit_id = git_revision_hash()
```

# 生成业务流水号

``` python
from jkutils.env import EnvZk
from jkutils.ids import serial_number

ez = EnvZk("127.0.0.1:2181", "chaos", "localhost:12345")
# ez.zk_node_number 获取 zk node 节点名称后 7 位数字
sn = serial_number("1020", ez.zk_node_number, "00001")
print("=====sn=======", sn) # 10200000012000013178922453168129
```

# rabbit MQ 消息推送

``` python
from jkutils.rabbitmq import MQPublisher

p = MQPublisher("amqp://xxx:xxx@127.0.0.1:111/")
p.publish(exchange="test", exchange_type="topic", durable=True, routing_key="teddy", msg="xxx",properties={"delivery_mode":2})

```
