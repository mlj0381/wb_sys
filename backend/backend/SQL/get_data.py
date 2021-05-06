from .base_sql import Basic_opear as sql
from . import  settings
from .check_statu import statu
from .functions.lasting_time import get_time
from .functions.get_date import reckon as get_date
import pymongo
import re
# 暂为多电脑可同时登录一个账户
# 后期更新


class get_data(object):

    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)

    def get_Ch_id(self,Ch_name):
        db = self.myclient['ch_info']
        table = db['ch_info']
        name = table.find({"Ch_name":Ch_name})
        if(name.count()):
            return name[0]['Ch_id']
        else:
            return False

    def get_Ch_name(self,Ch_id):
        db = self.myclient['ch_info']
        table = db['ch_info']
        name = table.find({"Ch_id": Ch_id})
        if (name.count()):
            return name[0]['Ch_name']
        else:
            return False

    def get_analysis_data(self,Ch_name,date,cookie):
        db = self.myclient['user_info']
        if(Ch_name == '全部'):
            user_id = statu().get_name(cookie)['user_id']
            if(date == '0'):
                table = db['user_week_info']
                return table.find({"account":user_id})[0]
            elif(date == '1'):
                table = db['user_month_info']
                return table.find({"account": user_id})[0]
            elif (date == '2'):
                table = db['user_all_info']
                return table.find({"account": user_id})[0]
        else:
            Ch_id = self.get_Ch_id(Ch_name)
            if(Ch_id):
                if(date == '0'):
                    table = db['ch_week_info']
                    return table.find({"Ch_id":Ch_id})[0]
                if (date == '1'):
                    table = db['ch_month_info']
                    return table.find({"Ch_id": Ch_id})[0]
                if (date == '2'):
                    table = db['ch_all_info']
                    return table.find({"Ch_id": Ch_id})[0]
            else:
                return False

   # 获得用户超话队列

    def get_Chid(self,user_id):
        array = []
        db = self.myclient['user_info']
        table = db['user_task']
        data = table.find({"account":user_id})
        for i in data:
            array.append(i['Ch_id'])
        return array


    def get_iniv_number(self,Ch_name,date,attitude,key_word,cookie):

        time = get_time().main(1)[0]
        date = int(date)
        attitude = int(attitude)
        if (date == 0):
            times = [time]
        elif (date == 1):
            times = get_date().main([time, 3])
        elif (date == 2):
            times = get_date().main([time, 7])
        elif (date == 3):
            times = get_date().main([time, 30])
        elif (date == 4):
            times = get_date().main([time, 360])

        if (Ch_name == '全部'):
            user_id = statu().get_name(cookie)['user_id']
            Ch_id = self.get_Chid(user_id)
        else:
            Ch_id = [self.get_Ch_id(Ch_name)]


        db = self.myclient['spider']
        table = db['iniv_content_0405']
        number = 0
        if(attitude == 0):
            for time in times:
                for id in Ch_id:
                    datas = table.find({"iniv_content_text": re.compile(key_word), "iniv_date": re.compile(time),"Ch_id": id})
                    number += datas.count()
                    if(number > 1000):
                        break
                if(number>1000):
                    break
        if (attitude == 1):
            for time in times:
                for id in Ch_id:
                    datas = table.find(
                        {"iniv_content_text": re.compile(key_word), "iniv_date": re.compile(time), "Ch_id": id,"iniv_grade":{'$gte':0.99}})
                    number += datas.count()
                    if (number > 1000):
                        break
                if (number > 1000):
                    break
        elif (attitude == 2):
            for time in times:
                for id in Ch_id:
                    datas = table.find(
                        {"iniv_content_text": re.compile(key_word), "iniv_date": re.compile(time), "Ch_id": id,"iniv_grade":{'$gt': 0.05,'$lt':0.99}})
                    number += datas.count()
                    if (number > 1000):
                        break
                if (number > 1000):
                    break
        elif (attitude == 3):
            for time in times:
                for id in Ch_id:
                    datas = table.find(
                        {"iniv_content_text": re.compile(key_word), "iniv_date": re.compile(time), "Ch_id": id,"iniv_grade":{'$lte':0.05}})
                    number += datas.count()
                    if (number > 1000):
                        break
                if (number > 1000):
                    break
        return (int(number/13) if number/13-int(number/13)==0 else int(number/13)+1)

    def get_iniv_data(self,key_word,page,times,Ch_id,attitude=0):
        print(page,times,key_word,Ch_id,attitude)
        page=int(page)
        attitude = int(attitude)

        db = self.myclient['spider']
        table = db['iniv_content_0405']
        data=[]
        number = 0
        for time in times:
            for id in Ch_id:
                if(attitude == 0):
                    datas = table.find({"iniv_content_text":re.compile(key_word),"iniv_date":re.compile(time),"Ch_id":id})
                    for i in datas:
                        i.pop('_id')
                        i['Ch_name'] = self.get_Ch_name(i['Ch_id'])
                        data.append(i)
                        number+=1
                        if(number >=page*10+10):
                            break
                elif(attitude == 1):
                    datas = table.find({"iniv_content_text": re.compile(key_word), "iniv_date": re.compile(time),"iniv_grade":{'$gte':0.99},"Ch_id":id})
                    for i in datas:
                        i.pop('_id')
                        i['Ch_name'] = self.get_Ch_name(i['Ch_id'])
                        data.append(i)
                        number += 1
                        if (number >= page * 10 + 10):
                            break
                elif (attitude == 2):
                    datas = table.find({"iniv_content_text": re.compile(key_word), "iniv_date": re.compile(time),
                                        "iniv_grade": {'$gt': 0.05,'$lt':0.99},"Ch_id":id})
                    for i in datas:
                        i.pop('_id')
                        i['Ch_name'] = self.get_Ch_name(i['Ch_id'])
                        data.append(i)
                        number += 1
                        if (number >= page * 10 + 10):
                            break
                elif (attitude == 3):
                    datas = table.find({"iniv_content_text": re.compile(key_word), "iniv_date": re.compile(time),
                                        "iniv_grade": {'$lte':0.05},"Ch_id":id})
                    for i in datas:
                        i.pop('_id')
                        i['Ch_name'] = self.get_Ch_name(i['Ch_id'])
                        data.append(i)
                        number += 1
                        if (number >= page * 10 + 10):
                            break
                if (number >= page * 10 + 10):
                    break
            if (number >= page * 10 + 10):
                break


        return [data[page * 10:number],100]


    def get_testing_data(self,Ch_name,date,page,keyword,attitude,cookie):
        db = self.myclient['spider']
        table = db['iniv_content_0405']

        time = get_time().main(1)[0]
        date=int(date)

        if (date == 0):
            times = [time]
        elif (date == 1):
            times = get_date().main([time,3])
        elif (date == 2):
            times = get_date().main([time,7])
        elif (date == 3):
            times = get_date().main([time,30])
        elif (date == 4):
            times = get_date().main([time,360])

        if(Ch_name == '全部'):
            user_id = statu().get_name(cookie)['user_id']
            Ch_id = self.get_Chid(user_id)
            data = self.get_iniv_data(keyword,page,times,Ch_id,attitude)
        else:
            Ch_id = [self.get_Ch_id(Ch_name)]
            if(Ch_id):
                data = self.get_iniv_data(keyword, page, times, Ch_id, attitude)
            else:
                return False


        return data





    def get_view_data(self,cookie):
        user_id = statu().get_name(cookie)['user_id']
        Ch_id=self.get_Chid(user_id)
        Ch_array = []
        db = self.myclient['user_info']
        table = db['ch_week_info']
        for id in Ch_id:
            data = table.find({"Ch_id":id})
            if(data.count()):
                Ch_name = self.get_Ch_name(data[0]['Ch_id'])
                Ch_array.append([Ch_name,data[0]['post:num'],data[0]['comment_num'],data[0]['grade']])

        db = self.myclient['ch_info']
        table = db['ch_update_info']
        for index,id in enumerate(Ch_id):
            time = get_time().main(1,id)[0]
            data = table.find({"Ch_id":id,"update_time": re.compile(time)})
            if(data.count()):
                Ch_array[index].append([data[0]['post_num'],data[0]['read_num'],data[0]['follow_num']])

        table = db['ch_info']
        for index,id in enumerate(Ch_id):
            img = table.find({"Ch_id":id})[0]['img']
            Ch_array[index].append(img)

        Ch_array = sorted(Ch_array,key=lambda x:x[1],reverse=True)
        return Ch_array


    def get_hot_data(self,cookie,Ch_name,date):
        array = []
        if(Ch_name == '全部'):
            user_id = statu().get_name(cookie)['user_id']
            db = self.myclient['user_info']
            if (date == '0'):
                table = db['user_week_info']
            if (date == '1'):
                table = db['user_month_info']
            if (date == '2'):
                table = db['user_all_info']
            data = table.find({"account": user_id})
            for index,i in enumerate(data[0]['hot_words']):
                if(index == 9):
                    break
                array.append(i)
        else:
            Ch_id = self.get_Ch_id(Ch_name)

            db = self.myclient['user_info']
            if (date == '0'):
                table = db['ch_week_info']
            if (date == '1'):
                table = db['ch_month_info']
            if (date == '2'):
                table = db['ch_all_info']
            data = table.find({"Ch_id": Ch_id})
            for index, i in enumerate(data[0]['hot_words']):
                if (index == 9):
                    break
                array.append(i)

        array = sorted(array,key=lambda  x:x[1])

        hot_array = [[]]

        number = 10
        for index,i in enumerate(array):
            hot_array.append([number+index*10,i[1],i[0]])

        return hot_array







    def get_home_data(self,user_id):
        db = self.myclient['user_info']
        table = db['user_home']
        data = table.find({"account":user_id})[0]
        data.pop('_id')
        return data


    def get_task_queue(self,cookie):
        user_id = statu().get_name(cookie)['user_id']
        db = self.myclient['user_info']
        table = db['user_task']
        data = table.find({'account':user_id})
        array = []
        for i in data:
            array.append([i['Ch_name'],i['Ch_id'],i['insert_time']])
        db = self.myclient['ch_info']
        table = db['ch_info']
        for index,i in enumerate(array):
            print(i)
            data = table.find({"Ch_id":i[1]})
            array[index].append(data[0]['statu'])

        for index,i in enumerate(array):
            data = get_time().main(1,i[1])
            if(data):
                array[index].append(data[0])
            else:
                array[index].append("暂无日期")

        return array
