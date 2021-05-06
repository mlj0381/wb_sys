import pymongo
import re

from update_py import settings
from update_py.lasting_time import get_time
from update_py.base_info import base_info
from update_py.active_user import active_user
from update_py.hot_word import hot_words
from update_py.map import map
from update_py.comment_grade import comment_grade
from update_py.functions.get_date import reckon
from update_py.sex_age import sex_age
#每日更新超话信息
from update_py.daily_data_update import data_update


class home_update(object):
    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)

    def get_user(self):
        user = []
        db =self.myclient['user_info']
        table = db['account']
        data = table.find()
        for i in data:
            user.append(i['account'])
        return user

    def get_task(self,user_id):
        ch_id = []
        db =self.myclient['user_info']
        table = db['user_task']
        data = table.find({'account':user_id})
        for i in data:
            ch_id.append(i['Ch_id'])
        return ch_id

    def get_ch_queue(self):
        db = self.myclient['ch_info']
        table = db['ch_info']
        array = []
        for i in table.find():
            array.append(i['Ch_id'])
        return array

    def ch_rank(self,ch_id):
        db = self.myclient['ch_info']
        table = db['one_day']
        array=[]
        for id in ch_id:
            data = table.find({"Ch_id":id})
            if(data.count()):
                array.append([data[0]['Ch_id'],data[0]['post_num'],data[0]['read_num']])
        table = db['ch_info']
        for i in range(len(array)):
            if(i==5):
                break
            data = table.find({"Ch_id":array[i][0]})
            array[i].append(data[0]['Ch_name'])
            array[i].append(data[0]['img'])

        array = sorted(array,key=lambda x : x[2],reverse=True)
        return array

    def one_day_update(self):
        data_update().main()
        user = self.get_user()
        for i in user:
            task = self.get_task(i)
            # 日常任务处理
            time = get_time().main(2)
            # 发帖量 阅读数 新增关注度 评论量 言论指数 超话检测数
            baseinfo = base_info().main(time, task)

            base2info = comment_grade().main([time[0]], task)

            baseinfo.append(len(task))
            # 超话排行榜
            ch_rank = self.ch_rank(task)
            # 活跃用户
            activeuser = active_user().main([time[0]], task)
            # 今日热词
            hotwords = hot_words().main([time[0]], task)
            # 今日地区
            area = map().main([time[0]], task)
            db = self.myclient['user_info']
            table = db['user_home']
            data = table.find({"account": i})
            if (data.count() == 0):
                table.insert({"account": i, "update_time": time[0], "post_num": baseinfo[0], "read_num": baseinfo[1],
                              "follo_num": baseinfo[2],
                              "comment_num": base2info[0], "grade": base2info[1], "ch_num": baseinfo[3],
                              "rank": ch_rank, "active_user": activeuser,
                              "hot_words": hotwords, "area": area, "post_analy": base2info[2]})
            else:
                table.update({"account": i}, {
                    '$set': {"update_time": time[0], "post_num": baseinfo[0], "read_num": baseinfo[1],
                             "follo_num": baseinfo[2],
                             "comment_num": base2info[0], "grade": base2info[1], "ch_num": baseinfo[3], "rank": ch_rank,
                             "active_user": activeuser,
                             "hot_words": hotwords, "area": area, "post_analy": base2info[2]}})

    def weekend_update(self):
        time = get_time().main(1)[0].split('-')
        now_time = []
        for i in time:
            try:
              k = int(i)
            except:
              k = int(i.split('0')[1])
            now_time.append(k)
        times = reckon().main([now_time[0],now_time[1],now_time[2],7])

        user = self.get_user()

        for i in user:
            task = self.get_task(i)
            week_data=[]
            baseinfo1 = comment_grade().main(times, task)
            baseinfo1[2] = comment_grade().get_data_analysis2(times,task)
            hotwords = hot_words().main(times, task)
            mapinfo = map().main(times, task)
            sexinfo=sex_age().main(times,task)
            db = self.myclient['user_info']
            table = db['user_week_info']

            if(table.find({"account":i}).count()):
                table.update({"account":i},{'$set':{"update_time":times[0],"post:num":baseinfo1[3],"comment_num":baseinfo1[0],"grade":baseinfo1[1],"active_time":baseinfo1[2],
                   "hot_words":hotwords,"map":mapinfo,"sex_ratio":sexinfo[0],"age":sexinfo[1]}})
            else:
                table.insert({"account":i,"update_time":times[0],"post:num":baseinfo1[3],"comment_num":baseinfo1[0],"grade":baseinfo1[1],"active_time":baseinfo1[2],
                   "hot_words":hotwords,"map":mapinfo,"sex_ratio":sexinfo[0],"age":sexinfo[1]})


    def months_update(self):
        time = get_time().main(1)[0].split('-')
        now_time = []
        for i in time:
            try:
                k = int(i)
            except:
                k = int(i.split('0')[1])
            now_time.append(k)
        times = reckon().main([now_time[0], now_time[1], now_time[2], 30])

        user = self.get_user()

        for i in user:
            task = self.get_task(i)
            week_data = []
            baseinfo1 = comment_grade().main(times, task)
            baseinfo1[2] = comment_grade().get_data_analysis2(times, task)
            hotwords = hot_words().main(times, task)
            mapinfo = map().main(times, task)
            sexinfo = sex_age().main(times, task)

            db = self.myclient['user_info']
            table = db['user_month_info']

            if (table.find({"account": i}).count()):
                table.update({"account": i}, {
                    '$set': {"update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                             "grade": baseinfo1[1], "active_time": baseinfo1[2],
                             "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]}})
            else:
                table.insert(
                    {"account": i, "update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                     "grade": baseinfo1[1], "active_time": baseinfo1[2],
                     "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]})

    def all_update(self):
        time = get_time().main(1)[0].split('-')
        now_time = []
        for i in time:
            try:
                k = int(i)
            except:
                k = int(i.split('0')[1])
            now_time.append(k)
        timess = reckon().main([now_time[0], now_time[1], now_time[2], 1000])
        times=['']
        user = self.get_user()

        for i in user:
            task = self.get_task(i)
            week_data = []
            baseinfo1 = comment_grade().main(times, task)
            baseinfo1[2] = comment_grade().get_data_analysis2(timess, task)
            hotwords = hot_words().main(times, task)
            mapinfo = map().main(times, task)
            sexinfo = sex_age().main(times, task)

            db = self.myclient['user_info']
            table = db['user_all_info']

            if (table.find({"account": i}).count()):
                table.update({"account": i}, {
                    '$set': {"update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                             "grade": baseinfo1[1], "active_time": baseinfo1[2],
                             "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]}})
            else:
                table.insert(
                    {"account": i, "update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                     "grade": baseinfo1[1], "active_time": baseinfo1[2],
                     "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]})


    def ch_week_update(self,task):
        time = get_time().main(1)[0].split('-')
        now_time = []
        for i in time:
            try:
                k = int(i)
            except:
                k = int(i.split('0')[1])
            now_time.append(k)
        times = reckon().main([now_time[0], now_time[1], now_time[2], 7])


        week_data = []
        baseinfo1 = comment_grade().main(times, task)
        baseinfo1[2] = comment_grade().get_data_analysis2(times, task)
        hotwords = hot_words().main(times, task)
        mapinfo = map().main(times, task)
        sexinfo = sex_age().main(times, task)

        db = self.myclient['user_info']
        table = db['ch_week_info']

        if (table.find({"Ch_id": task[0]}).count()):
            table.update({"Ch_id": task[0]}, {
                '$set': {"update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                         "grade": baseinfo1[1], "active_time": baseinfo1[2],
                         "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]}})
        else:
            table.insert(
                {"Ch_id": task[0], "update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                 "grade": baseinfo1[1], "active_time": baseinfo1[2],
                 "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]})

    def ch_month_update(self,task):
        time = get_time().main(1)[0].split('-')
        now_time = []
        for i in time:
            try:
                k = int(i)
            except:
                k = int(i.split('0')[1])
            now_time.append(k)
        times = reckon().main([now_time[0], now_time[1], now_time[2], 30])


        week_data = []
        baseinfo1 = comment_grade().main(times, task)
        baseinfo1[2] = comment_grade().get_data_analysis2(times, task)
        hotwords = hot_words().main(times, task)
        mapinfo = map().main(times, task)
        sexinfo = sex_age().main(times, task)
        db = self.myclient['user_info']
        table = db['ch_month_info']

        if (table.find({"Ch_id": task[0]}).count()):
            table.update({"Ch_id": task[0]}, {
                '$set': {"update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                         "grade": baseinfo1[1], "active_time": baseinfo1[2],
                         "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]}})
        else:
            table.insert(
                {"Ch_id": task[0], "update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                 "grade": baseinfo1[1], "active_time": baseinfo1[2],
                 "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]})

    def ch_all_update(self,task):
        time = get_time().main(1)[0].split('-')
        now_time = []
        for i in time:
            try:
                k = int(i)
            except:
                k = int(i.split('0')[1])
            now_time.append(k)
        timess = reckon().main([now_time[0], now_time[1], now_time[2], 1000])
        times=['']

        week_data = []
        baseinfo1 = comment_grade().main(times, task)
        baseinfo1[2] = comment_grade().get_data_analysis2(timess, task)
        hotwords = hot_words().main(times, task)
        mapinfo = map().main(times, task)
        sexinfo = sex_age().main(times, task)


        db = self.myclient['user_info']
        table = db['ch_all_info']

        if (table.find({"Ch_id": task[0]}).count()):
            table.update({"Ch_id": task[0]}, {
                '$set': {"update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                         "grade": baseinfo1[1], "active_time": baseinfo1[2],
                         "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]}})
        else:
            table.insert(
                {"Ch_id": task[0], "update_time": times[0], "post:num": baseinfo1[3], "comment_num": baseinfo1[0],
                 "grade": baseinfo1[1], "active_time": baseinfo1[2],
                 "hot_words": hotwords, "map": mapinfo, "sex_ratio": sexinfo[0], "age": sexinfo[1]})



    def main(self,times=False,Ch_id=False):
        self.one_day_update()
        self.weekend_update()
        self.months_update()
        self.all_update()
        task = self.get_ch_queue()
        for i in task:
            self.ch_week_update([i])
            self.ch_month_update([i])
            self.ch_all_update([i])



