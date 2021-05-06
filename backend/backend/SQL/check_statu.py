from .base_sql import Basic_opear as sql
from . import  settings
import pymongo
# 暂为多电脑可同时登录一个账户
# 后期更新


class statu(object):
    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)

    def check_cookie(self,cookie):
        if(sql().check_exist('user_info','cookie',{"cookie":cookie})):
            return True
        else:
            return False

    def get_Ch_name(self,user_id):
        array = []
        db = self.myclient['user_info']
        table = db['user_task']
        data = table.find({"account":user_id})
        for i in data:
            array.append(i['Ch_name'])
        return array

    def get_name(self,cookie):
        db = self.myclient['user_info']
        table = db ['cookie']
        user_id = table.find({"cookie":cookie})[0]['account']
        table = db['account']
        user_name = table.find({"account":user_id})[0]['name']
        user_id = table.find({"account":user_id})[0]['account']
        Ch_name = self.get_Ch_name(user_id)
        return {"user_name":user_name,"user_id":user_id,"Ch_name":Ch_name}



    def main(self,cookie):
        if(self.check_cookie(cookie)):
            user_info = self.get_name(cookie)
            return {'statu':1,"user_name":user_info['user_name'],"user_id":user_info["user_id"],"Ch_name":user_info["Ch_name"]}
        else:
            return False
