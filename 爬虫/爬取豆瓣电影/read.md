### 什么是数据库
数据库，简而言之可视为电子化的文件柜——存储电子文件的处所，用户可以对文件中的数据进行新增、查询、更新、删除等操作。






### Python DB-API使用流程：
- 引入 API 模块。
- 获取与数据库的连接。
- 执行SQL语句和存储过程。
- 关闭数据库连接。


###### 常见的数据库应该是mysql ，mongodb，redis
大家首先安装好mysql，mongodb，redis




### MySQL与Python的交互
在使用 PyMySQL 之前，我们需要确保 PyMySQL 已安装

`$ pip3 install PyMySQL` （打开cmd pip 安装）
现在我们开始来学习一下怎么连接操作mysql。

首先我们需要导入pymysql的模块，`import pymysql`。然后调用`pymysql.connect()`连接数据库。调用`connect`发回的游标`connection.cursor()`，执行查询语句。接下来我们需要调用`cursor.execute()`来执行sql语句，`connection.commit()`，最后调用`connection.close()`方法关闭数据库连接。

代码如下：
```
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost","testuser","test123","TESTDB" )
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询 
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
print ("Database version : %s " % data)
# 关闭数据库连接
db.close()
```
还有简便的写法
```python
import pymysql
db_config = {
    'user':'root',
    'password':'qwe123',
    'db':'spiders', #数据库名字
    'charset':'utf8'
    'host' : 'localhost' #虚拟机ip
}
db = pymysql.connect(**db_config)
cur = db.cursor()
#查找
cur.execute('select * from teacher_student')
# 插入
sql1 = 'insert into items(id,name,age) VALUES(%s,%s,%s)'
cur.execute(sql1,('1','毛利',18))
db.commit() #要提交
#改
sql2 = 'update items set age = %s where name = %s'
cursor.execute(sql2,(8888,'毛利'))
db.commit()
db.close()
```

###  mongodb与Python的交互

确保安装好pymongo

```
import pymongo
collection = pymongo.MongoClient()
db = collection['my_mongo'] 
my_col = db['student']
result = my_col.insert_one({'name':'毛利'},{'age':18})
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190318234334138.jpg)

### redis与Python的交互
redis的库不叫pyredis，叫redis
```
import redis
conn = redis.StrictRedis() #就是一个StrictRedis()
result = conn.get('name')
print(result)
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019031823434410.jpg)


### 实战爬取

爬取对象（豆瓣电影top250数据抓取并入mongodb数据库）

> https://movie.douban.com/top250?start=25&filter=


![爬取的数据](https://img-blog.csdnimg.cn/20190720231815190.png)




- 封装数据库



```
# 封装monongodb
import pymongo
from pymongo.collection import Collection
class Handle_Mongo(object):
    def __init__(self):
        # 虚拟机的ip是192.168.96.128
        mongo_client = pymongo.MongoClient(host="192.168.96.128",port=27017)
        # 数据库的名称
        self.db_data = mongo_client['douban']
    def handle_save_data(self,item):
        # 集合的名字
        task_collection = Collection(self.db_data,'douban_data')
        # 插入数据
        task_collection.insert(item)
douban_mongo = Handle_Mongo()

```

这次爬虫使用多线程的方法

```
import re
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree
from handle_mongo import douban_mongo

```
分析url发现start这个参数在变化，所以不断的迭代
```
def handle_page_url(self):
        #通过分析页面URL可以得知
        #通过range构造页码变量,从0开始,到249结束,步长为25
        for i in range(0,250,25):
            url = "https://movie.douban.com/top250?start=%s&filter="%i
            self.page_url.append(url)
```

不断的用xpath来解析
```
    def handle_page_detail(self,url):
        # print(url)
        #处理特殊字符
        sub_search = re.compile(r"[\s\r\t]")
        response = self.handle_request(url=url)
        html = etree.HTML(response)
        #解析当前页面有多少个电影信息
        item_list = html.xpath("//ol[@class='grid_view']//li")
        print(item_list)
        for item in item_list:
            info = {}
            #电影名称,将特殊字符替换为空
            info['movie_name'] = sub_search.sub('',''.join(item.xpath(".//div[@class='hd']/a//span/text()")))
            info['actors_information'] = sub_search.sub('',''.join(item.xpath(".//div[@class='bd']/p/text()")))
            info['score'] = sub_search.sub('',''.join(item.xpath(".//div[@class='bd']/div[@class='star']/span[2]/text()")))
            info['evaluate'] = sub_search.sub('',''.join(item.xpath(".//div[@class='bd']/div[@class='star']/span[4]/text()")))
            info['describe'] = sub_search.sub('',''.join(item.xpath(".//p[@class='quote']/span/text()")))
            info['from_url'] = url
            #数据入库
            # print(info)
            douban_mongo.handle_save_data(info)
```

开多线程爬虫
```
#启动方法
def run(self):
    self.handle_page_url()
    #创建线程池
    t = ThreadPoolExecutor()
    for i in self.page_url:
        t.submit(self.handle_page_detail,i)
    t.shutdown()
    print(self.page_url)
```


![效果图](https://img-blog.csdnimg.cn/20190720232642102.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDUxMDYxNQ==,size_16,color_FFFFFF,t_70)


在公众号回复：[ 豆瓣] 获得本文全代码



