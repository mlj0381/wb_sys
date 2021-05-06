import time
import redis
import pymongo
from update_py import settings
from home_update import home_update as update
while(True):
    if(list(time.localtime())[3]%6==0):
        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db = myclient['ch_info']
        table = db['ch_info']
        print('begin')
        redis_link = redis.StrictRedis(host=settings.REDIS_URL, port=6379, db=0)
        data = table.find()
        for i in data:
            if(i['statu'] == 1):
                url = 'https://weibo.com/p/'+i['Ch_id']
                redis_link.lpush('ch_queue',url)
        time.sleep(3600)
        redis_link.lpush('home_queue','https://www.baidu.com')
        time.sleep(300)
        update().main()
        
    print("now time:")
    print(time.localtime())
    time.sleep(60)
