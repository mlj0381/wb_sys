# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WbSysItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class iniv_info(scrapy.Item):
    #超话id
    Ch_id = scrapy.Field()
    #日期
    iniv_date = scrapy.Field()
    #表情包
    iniv_expre = scrapy.Field()
    #帖子链接
    iniv_url = scrapy.Field()
    #帖子id
    iniv_id = scrapy.Field()
    #帖子内容
    iniv_content_text = scrapy.Field()
    #转发数
    iniv_forward_num = scrapy.Field()
    #评论数
    iniv_comment_num = scrapy.Field()
    #点赞数
    iniv_prase_num = scrapy.Field()
    #发帖人头像
    iniv_post_img = scrapy.Field()
    #发帖人id
    iniv_post_id = scrapy.Field()
    #发帖人名字
    iniv_post_name = scrapy.Field()
    #情感等级
    iniv_grade = scrapy.Field()

class user_info(scrapy.Item):
    #超话ID
    Ch_id = scrapy.Field()
    #用户昵称
    user_name = scrapy.Field()
    #用户ID
    user_id = scrapy.Field()
    #用户头像
    user_img = scrapy.Field()
    #用户年龄
    user_sex = scrapy.Field()
    #用户年龄
    user_age = scrapy.Field()
    #用户注册日期
    user_resig_data = scrapy.Field()
    #用户所在地
    user_region = scrapy.Field()
