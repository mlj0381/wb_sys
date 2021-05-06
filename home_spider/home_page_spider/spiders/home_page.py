import scrapy
import pymongo
import re
import time
from .. import settings
from ..items import update_info
from scrapy_redis.spiders import RedisSpider
from .. import settings
import redis


class HomePageSpider(RedisSpider):
    name = 'home_page'
    redis_key = 'home_queue'


    def parse(self,response):
        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db = myclient['ch_info']
        table = db['ch_info'].find()
        task_queue = []
        for i in table:
            if(i['statu']==1):
                task_queue.append(i['Ch_id'])
        for i in task_queue:
            url='https://weibo.com/p/' + i +'/super_index'
            yield scrapy.Request(url=url,callback=self.parse2,meta={"Ch_id":i},dont_filter=True)

 
    def parse2(self,response):
        info = update_info()
        s= re.findall(r'阅读:(.*?),帖子:(.*?),粉丝:',response.text)
        t = re.findall(r'<strong class(.*?)">(.*?)<\\/strong><span class=\\"S_txt', response.text)[2][1]
        if('万' in t):
            t = int(float(re.findall('(.*?)万', t)[0]) * 1000)
        elif('亿' in t):
            t = int(float(re.findall('(.*?)万', t)[0]) * 100000000)
        Ch_id = re.findall(r'https://weibo.com/p/(.*?)/super_index',response.url)[0]
        check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        img = re.findall(r'mg src=\\"(.*?)\\" alt=\\"\\" title=\\"\\" class=\\"pic',response.text)

        info['Ch_id'] = Ch_id
        info['read_num'] = s[0][0]
        info['post_num'] = s[0][1]
        info['follow_num'] = t
        info['update_time'] = check_time
        yield info

        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db = myclient['ch_info']
        table = db['ch_info']
        table.update({"Ch_id":response.meta['Ch_id']},{'$set':{"img":img[0]}})
        

        

        
        
        
        

