import pymongo
from . import  settings
import re




from .functions.get_date import reckon
class data_update(object):
    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)

    def lasting_date(self,Ch_id=False):
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
                array.append(i)
            if(len(array)==2):
                break
        return array

    def update_data(self,Ch_id):
        array = self.lasting_date(Ch_id)
        if( len(array) == 2 ):
            read_num = int(array[0]['read_num']) - int(array[1]['read_num'])
            post_num = int(array[0]['post_num']) - int(array[1]['post_num'])
            follow_num = int(array[0]['follow_num']) - int(array[1]['follow_num'])
            time = array[0]['update_time'].split(" ")[0]
            db = self.myclient['spider']
            table = db['iniv_content_0405']
            comment = table.find({"iniv_date": re.compile(time),"Ch_id":Ch_id})
            number = table.find({"iniv_date": re.compile(time),"Ch_id":Ch_id},{"iniv_comment_num":1}).count()
            comment_num = 0
            grade = 0
            for i in comment:
                comment_num += int( i['iniv_comment_num'])
                grade += float(i['iniv_grade'])
            if(grade == 0 ):
                grade = 1
            else:
                grade = grade / number
            db = self.myclient['ch_info']
            table = db['one_day']
            if(table.find({"Ch_id":Ch_id}).count()):
                table.update({"Ch_id":Ch_id}, {'$set': {"read_num":read_num,"post_num":post_num,"follow_num":follow_num,'comment_num':comment_num,'grade':grade}})
            else:
                table.insert({"Ch_id":Ch_id,"read_num":read_num,"post_num":post_num,"follow_num":follow_num,"comment_num":comment_num,"grade":grade})
        else:
            return False


    def main(self):
        db=self.myclient['ch_info']
        table = db['ch_info']
        data = table.find({},{"Ch_id":1})
        for i in data:
            self.update_data(i['Ch_id'])


