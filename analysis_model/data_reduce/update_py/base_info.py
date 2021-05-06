import pymongo
from . import settings
import re
from .lasting_time import get_time
from .functions.get_date import reckon

class base_info(object):
    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)


    def map_dic(self):
        array={}
        with open('./word_type/region.txt','r',encoding='utf8') as file:
            for i in file:
                array[i.strip()] = 0
        return array

    def get_data(self,times,Ch_id):
        post =0
        read =0
        follow =0
        array = []
        db = self.myclient['ch_info']
        table = db['ch_update_info']
        for id in Ch_id:
            datas = []
            for time in times:
                data = table.find({"Ch_id":id,"update_time":re.compile(time)})
                if(data.count()):
                    datas.append(sorted(data,key= lambda x:x['update_time'],reverse=True)[0])
            if(len(datas) >= 2):
                array.append(datas)
        for i in array:
            i = sorted(i,key=lambda x:x['update_time'],reverse=True)
            post += int(i[0]['post_num']) - int(i[len(i)-1]['post_num'])
            read += int(i[0]['read_num']) - int(i[len(i)-1]['read_num'])
            follow += int(i[0]['follow_num']) - int(i[len(i)-1]['follow_num'])
        return [post,read,follow]







    def get_times(self,num):
        lasting_date = get_time().main(1)[0].split('-')
        print(lasting_date)
        times = reckon().main([lasting_date[0], lasting_date[1], lasting_date[2], num])
        return times

    # 输入日期获得地区 必须
    # 超话id   must
    #  参数 （ 最近几天 ， 超话 id）

    def main(self,times,Ch_id):
       # times = self.get_times(num)
        return self.get_data(times,Ch_id)

