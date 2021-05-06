from . import settings
import pymongo
import re

class active_user(object):
    def __init__(self):
        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db = myclient['spider']
        self.table = db['iniv_content_0405']

    def active_most(self,times,Ch_id):
        counts = {}
        for time in times:
            for id in Ch_id:
                data = self.table.find({"Ch_id":id,"iniv_date": re.compile(time)},{"iniv_post_id":1,"iniv_grade":1})
                for i in data:
                    counts[i['iniv_post_id']] = counts.get(i['iniv_post_id'], 0) + 1
        items = list(counts.items())
        if(len(items)):
            grade = 0
            items.sort(key=lambda x: x[1], reverse=True)
            data = self.table.find({"iniv_post_id": items[0][0]})
            user_info = data[0]
            for i in data:
                grade += float(i['iniv_grade'])
            grade =grade/data.count()
            return [items[0][0],items[0][1],user_info['iniv_post_name'],user_info['iniv_post_img'],grade]
        else:
            return False

    def main(self,times,Ch_id=False):
        return self.active_most(times,Ch_id)

