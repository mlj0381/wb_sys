import pymongo
from . import  settings

#     Mongodb
#    基础操作，增删改查

class Basic_opear(object):
    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)

    #增
    # 参数（库名,表名,数据）
    def insert(self,db,table,data):
        db = self.myclient[db]
        table = db[table]
        table.insert_one(data)


    #删
    #暂时不用
    ###############################

    #改
    # 参数（库名,表名,索引条件，更改数据）
    def update(self,db,table,index,data):
        db = self.myclient[db]
        table = db[table]
        table.update(index,{'$set':data})

    # 查
    # 参数（库名,表名,数据）
    def check_exist(self,db,table,data):
        db = self.myclient[db]
        table = db[table]
        if(table.find(data).count()):
            return True
        else:
            return False







