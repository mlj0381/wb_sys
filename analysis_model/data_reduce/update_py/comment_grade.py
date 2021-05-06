from . import settings
import pymongo
import re
from .lasting_time import get_time



class comment_grade(object):
    def __init__(self):
        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db = myclient['spider']
        self.table = db['iniv_content_0405']

    def active_most(self,times,Ch_id):
        comment = 0
        grade = 0
        number = 0
        for time in times:
            for id in Ch_id:
                data = self.table.find({"Ch_id":id,"iniv_date": re.compile(time)},{"iniv_comment_num":1,"iniv_grade":1})
                for i in data:
                    number+=1
                    comment +=int(i['iniv_comment_num'])
                    grade += float(i['iniv_grade'])

        post_analysis=self.get_data_analysis(Ch_id)
        return [comment*20,float('%.3f' % (grade/number)),post_analysis,number] if grade!=0 else [comment,1,post_analysis,number]

    def get_data_analysis(self,Ch_id):
        times=get_time().main(7)
        array=[]
        for time in times:
            days = 0
            for id in Ch_id:
                days += self.table.find({"Ch_id":id,"iniv_date": re.compile(time)}).count()
            array.append([time,days])
        return (sorted(array,key=lambda x:x[0]))

    def get_data_analysis2(self,times,Ch_id):
        array = []
        for time in times:
            days = 0
            for id in Ch_id:
                days += self.table.find({"Ch_id": id, "iniv_date": re.compile(time)}).count()
            array.append([time, days])
        dic = dict(sorted(array, key=lambda x: x[0]))
        return ({"x":list(dic.keys()),"y":list(dic.values())})


    def main(self,times,Ch_id=False):
        return self.active_most(times,Ch_id)
