import requests
import redis
import re
import time
import pymongo
from . import settings
from .base_sql import Basic_opear as sql
from .check_statu import statu as get

class check_name(object):
    def __init__(self):
        self.redis_link = redis.StrictRedis(host=settings.REDIS_URL)
        self.cookie = self.redis_link.get('cookie')
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)

    def get_Ch_id(self,Ch_name):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
        }

        url = 'https://s.weibo.com/weibo?q=' + Ch_name
        print(url)

        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            r.encoding = 'utf-8'
            info = re.findall(r'a href="http://weibo.com/p/(.*?)" title="" target="_blank">(.*?)</a></h2>',r.text)
            print(info)
            if(info):
                if(info[0][1] == Ch_name):
                    print(info)
                    return info[0][0]
                else:
                    return False
            else:
                return False
        except:
            return False

    def check(self,Ch_name):
        for i in range(1):
            Ch_id = self.get_Ch_id(Ch_name)
            if(Ch_id):
                return Ch_id
        return False

    def check_exit(self,User_id,Ch_name):
        check_result=sql().check_exist('user_info','user_task',{'account':str(User_id),'Ch_name':Ch_name})
        if(check_result):
            return True
        else:
            return False

    def insert_task(self,Ch_name,Ch_id):
        if(not sql().check_exist('ch_info','ch_info',{'Ch_id':Ch_id})):
            check_result = sql().insert('ch_info',"ch_info",{"Ch_name":Ch_name,"Ch_id":Ch_id,'statu':1})

    def main(self,cookie,Ch_name):
        user_id = get().get_name(cookie)['user_id']
        if(not self.check_exit(user_id,Ch_name)):
            statu = self.check(Ch_name)
            if(statu):
                self.insert_task(Ch_name,statu)
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                sql().insert('user_info','user_task',{"account":user_id,"Ch_name":Ch_name,"Ch_id":statu,"insert_time":times})
                url = 'https://weibo.com/p/'+ statu
                self.redis_link.lpush('ch_queue',url)
                self.redis_link.lpush('home_queue','https://www.baidu.com')
                db = self.myclient['user_info']
                table = db['ch_week_info']
                table.insert({"Ch_id":statu,"grade":1,"comment_num":0,"post:num":0})
                return 1
            else:
                return 0
        else:
            return -1


