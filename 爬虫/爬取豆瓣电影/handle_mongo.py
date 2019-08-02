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
