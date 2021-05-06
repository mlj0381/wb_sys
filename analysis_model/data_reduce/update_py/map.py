import pymongo
from . import settings
import re

class map(object):
    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)


    def map_dic(self):
        array={}
        with open('./update_py/word_type/region.txt','r',encoding='utf8') as file:
            for i in file:
                array[i.strip()] = 0
        return array

    def get_time(self,times,Ch_id):
        array = self.map_dic()
        db = self.myclient['spider']
        for time in times:
            for id in Ch_id:
                table = db['iniv_content_0405']
                iniv = table.find({"iniv_date": re.compile(time),'Ch_id':id},{'iniv_post_id':1})
                table = db['iniv_user_0405']
                for i in iniv:
                    region = table.find({"user_id":i['iniv_post_id']},{"user_region":1})
                    if(region.count() and region[0]['user_region'] in array.keys()):
                        array[region[0]['user_region']]+=1
        return dict(sorted(array.items(),key=lambda x:x[1],reverse=True))

    def main(self,times,Ch_id=False):
        return self.get_time(times,Ch_id)

#输入日期获得地区 必须
#超话id   must


