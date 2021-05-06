# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from . import  settings

class HomePageSpiderPipeline(object):
    def __init__(self):
        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db=myclient['ch_info']
        self.table = db['ch_update_info']

    def process_item(self, item, spider):
        self.table.insert_one(dict(item))
        return item
