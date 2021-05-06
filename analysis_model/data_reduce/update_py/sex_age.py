from . import settings
import pymongo
import re

class sex_age(object):
    def __init__(self):
        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db = myclient['spider']
        self.table1 = db['iniv_content_0405']
        self.table2 = db['iniv_user_0405']

    def active_most(self,times,Ch_id):
        user = []
        counts={}
        boy = 0
        girl = 0
        for time in times:
            for id in Ch_id:
                data = self.table1.find({"Ch_id":id,"iniv_date":re.compile(time)})
                for i in data:
                    if(i['iniv_post_id'] not in user):
                        user.append(i['iniv_post_id'])

        for account in user:
            data = self.table2.find({"user_id":account})
            if(data.count()):
                if(data[0]['user_sex'] == '男'):
                    boy += 1
                if(data[0]['user_sex'] == '女'):
                    girl +=1
                if(data[0]['user_age'] != '未知' and data[0]['user_age'] <=40 and data[0]['user_age'] >=12):
                    counts[data[0]['user_age']] = counts.get(data[0]['user_age'],0) + 1

            counts = dict(sorted(counts.items(),key=lambda x:x[0]))

        k=[]
        for i in list(counts.items()):
            k.append(list(i))

        return [[boy,girl],k]

    def main(self,times,Ch_id=False):
        return self.active_most(times,Ch_id)

