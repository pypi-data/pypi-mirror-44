# cronjob 

---

### Overview

`cronjob`是一个轻量、分布式、异步的定时任务框架，主要参考`scrapy`，`rq`，异步主要基于gevent。所有的定时任务都会在`gevent`的微线程中执行。

---

### Installation

pip install cronjob

pip install git+https://github.com/havefun-plus/cronjob.git



---

### Usage

#### 1. settings

通过环境变量`CRONJOB_SETTINGS`指定配置文件, 配置见`settings.example.py`

* 通过`CRONJOBS_MODULE = 'cronjobs'`指定定时任务所在路径
* 通过`QUEUE_CONFIG = dict(queue_type='thread', config=None)`指定使用在什么模式运行
    * 指定redis，同时要指定redis配置
    * 指定thread，只能在单节点运行
    
参考： https://github.com/havefun-plus/ip-proxy-pool/blob/master/ipfeeder/settings.py
    
#### 2. 创建定时任务

参考：

* https://github.com/havefun-plus/ip-proxy-pool/blob/master/ipfeeder/cronjobs

* https://github.com/havefun-plus/cronjob/tree/master/examples

#### 3. 执行

单节点运行：

* `cronjob run`  默认一个线程调度任务，一个线程爬取
* `cronjob run --mode thread --num 2`  启动两个线程执行   

多节点运行：

注意只能增加`worker`实例，`master`实例只能为1

参考：

* https://github.com/havefun-plus/ip-proxy-pool/blob/master/deploy/master.sh

* https://github.com/havefun-plus/ip-proxy-pool/blob/master/deploy/worker.sh

---

### 项目参考:

eat your own dog food

基于`cronjob`实现的项目：

IP代理池

* https://github.com/havefun-plus/ip-proxy-pool

