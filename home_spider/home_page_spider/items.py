# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HomePageSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class update_info(scrapy.Item):
    #超话ID
    Ch_id = scrapy.Field()
    #发帖数
    post_num = scrapy.Field()
    #阅读数
    read_num = scrapy.Field()
    #关注数
    follow_num = scrapy.Field()
    #更新时间
    update_time = scrapy.Field()

