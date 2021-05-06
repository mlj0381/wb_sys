# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
#none
from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi

from .items import iniv_info,user_info



#   设置Mongodb数据库
class WegPipelineMon(object):
    def __init__(self):
        settings = get_project_settings()
        #设置Mongodb数据库参数
        db_url = settings['MONGO_URL']
        db_name = settings['MONGO_DATABASE']

        self.db_client = pymongo.MongoClient(db_url)
        self.db = self.db_client[db_name]
        

    #判断什么值
    def process_item(self, item, spider):
        #存储
        if isinstance(item,iniv_info):
            self.insert_iniv_info(item)
        else:
            self.insert_user_info(item)
        return item

    def insert_iniv_info(self,item):
        self.db.iniv_content_0405.insert_one(dict(item))

    def insert_user_info(self,item):
        if (not self.db.iniv_user_0405.find({"user_id": item['user_id']}).count()):
            self.db.iniv_user_0405.insert_one(dict(item))

