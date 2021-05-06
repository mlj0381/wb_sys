import pymongo
from . import settings

#获取最新发帖时间

class get_time():
    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)

    def lasting_date(self,Ch_id,num):
        table = self.myclient['ch_info']
        db = table['ch_update_info']
        if(Ch_id):
            db = db.find({"Ch_id":Ch_id})
        else:
            db =db.find()
        data = []
        for i in db:
            data.append(i)
        data=sorted(data,key = lambda x : x['update_time'],reverse = True)
        array = []
        for i in data:
            if(i['update_time'].split(" ")[0] not in str(array)):
                array.append(i['update_time'].split(" ")[0])
            if(len(array) == num):
                break
        return array

    def main(self,num=1,Ch_id=False):
        return self.lasting_date(Ch_id,num)
