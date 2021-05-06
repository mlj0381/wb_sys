import scrapy
import re
from scrapy_redis.spiders import RedisSpider
from .. import settings
import redis
import pymongo

from lxml import etree
from snownlp import SnowNLP
import time
from ..items import iniv_info,user_info

class WbSpider(RedisSpider):
    name = 'wb'
    #allowed_domains = ['weibo.com']
    #start_urls = ['http://weibo.com/']
    redis_key = 'ch_queue'

    def parse(self, response):
        print(response.url)
        Ch_id = re.findall(r'https://weibo.com/p/(.*)',response.url)[0]
        #page_num=int(re.findall(r'&countPage=(.*?)\\"',response.text)[0])
        page_num = 30
        for page_one in range(1,page_num+1):
            for page_box in range(-1,2):
                html="https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100808&current_page=8&since_id=4596180610459745&page="+str(page_one)+"&pagebar="+str(page_box)+"&tab=super_index&pl_name=Pl_Core_MixedFeed__262&id="+str(Ch_id)+"&script_uri=/p/100808bd58ae03303fe774c1b631c3b4a45d4f/super_index&feed_type=1&pre_page="+str(page_one)+"&domain_op=100808&__rnd=1613879856503"
                yield scrapy.Request(url=html,callback=self.get_post_One_url,meta={'Ch_id':Ch_id},dont_filter=True)


    def get_post_One_url(self,response):
        print("3")
        con=re.findall(r' <a target=\\"_blank\\" href=\\"(.*?)" title=\\"',response.text)
        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db=myclient['spider']
        table = db['iniv_content_0320']
        for id in con:
            url=id
            url=re.sub('\\\\','',url)
            print(url)
            if( db.iniv_content_0405.find({"iniv_url":url}).count()):
                print("It already exists")
            else:
                yield scrapy.Request(url=url,callback=self.get_iniv_info,meta={'Ch_id':response.meta['Ch_id']})

    def get_iniv_info(self,response):
        print("4")
        Ch_id = response.meta['Ch_id']
        main_text = re.findall(r'<div class=\\"WB_from S_txt2(.*?)<div class=\\"WB_like', response.text)
        if (main_text):
            t = main_text[0]
            xpaths = t.replace(r"\n", "").replace("\\", "")
            s = etree.HTML(xpaths)
            s = s.xpath('//div[@class="WB_text W_f14"]/text()')
            p = ""
            for i in s:
                if (i.replace(" ", "") != ""):
                    p = p + re.sub(r"\\|\n|\u200b| ", '', i)
            # 帖子日期
            iniv_date = re.findall(r'mod=weibotime\\" title=\\"(.*?)\\"', response.text)
            # 帖子内容
            iniv_expre = re.findall(r'alt=    "\[(.*?)\]" type="face"', xpaths)
            # 帖子id
            iniv_id = re.findall(r'&mid=(.*?)&', response.text)
            # 帖子转发数
            iniv_forward_num = re.findall(r"&#xe607;<\\/em><em>(.*?)<\\/em><\\/span>", response.text)
            # 帖子评论数
            iniv_comment_num = re.findall(r"&#xe608;<\\/em><em>(.*?)<\\/em><\\/spa", response.text)
            #发帖人头像
            self.iniv_post_img = re.findall(r'usercard(.*?)src=\\"(.*?)\?KID(.*?)width', response.text)[0][1].replace('\\', '')
            #  帖子获赞数
            iniv_prase_num = re.findall(r"ñ<\\/em><em>(.*?)<\\/em><\\/span>", response.text)
            # 发帖人id
            iniv_post_id = re.findall(r"\$CONFIG\['oid']='(.*?)'", response.text)
            # 发帖人昵称
            iniv_post_name = re.findall(r"\$CONFIG\['onick']='(.*?)'", response.text)
            if ('赞' in iniv_prase_num[0]):
                iniv_prase_num = ['0']
            if ('评论' in iniv_comment_num[0]):
                iniv_comment_num = ['0']
            if ('转发' in iniv_forward_num[0]):
                iniv_forward_num = ['0']

            #如果为转发的或者文字内容为空
            if(iniv_id and p!="" and p!="转发微博"):
                if (iniv_id and p != "" and p != "转发微博"):
                    item = iniv_info()
                    item['Ch_id'] = Ch_id
                    item['iniv_date'] = iniv_date[0]
                    item['iniv_url'] = response.url
                    item['iniv_id'] = iniv_id[0]
                    item['iniv_expre'] = iniv_expre
                    item['iniv_content_text'] = p
                    item['iniv_forward_num'] = iniv_forward_num[0]
                    item['iniv_comment_num'] = iniv_comment_num[0]
                    item['iniv_post_img'] = self.iniv_post_img
                    item['iniv_prase_num'] = iniv_prase_num[0]
                    item['iniv_post_id'] = iniv_post_id[0]
                    item['iniv_post_name'] = iniv_post_name[0]
                    grade = SnowNLP(p).sentiments
                    item['iniv_grade'] = grade
                    yield item
                    url="https://weibo.com/p/100505"+str(iniv_post_id[0])+"/info?mod=pedit_more"
                    yield scrapy.Request(url=url,callback=self.get_user_info,meta={'Ch_id':Ch_id})
    
    def get_user_info(self,response):
        print("5")
        Ch_id = response.meta['Ch_id']
        html=response.text
        content=str(re.findall(r'<span class=\\"pt_detail\\">[^\<]+',html))
        c=re.findall(r">(.*?)',",str(content))
        birth_day=re.findall(r"[\d]+年[\d]+月[\d]+日",str(content))
        logon_data=re.findall(r"[\d]+-[\d]+-[\d]+",str(content))
        if(len(birth_day)!=0):
            age=2021-int(re.findall(r"[\d]+",str(birth_day))[0])
        else:
            age="未知"
        if(len(c)!=0):
            print(c)
            item = user_info()
            item['Ch_id'] = Ch_id
            item['user_name']= c[0]
            item['user_id'] = re.findall(r"100505(.*?)/info?",response.url)[0]
            item['user_sex'] = c[2]
            item['user_img'] = self.iniv_post_img
            item['user_age'] = age
            item['user_resig_data'] = logon_data[0]
            item['user_region'] = c[1]
            yield item
        else:
            pass
