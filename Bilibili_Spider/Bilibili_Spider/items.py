# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# ---------- Item_Bilibili ----------
class BilibiliUserItem(scrapy.Item):
    id = scrapy.Field()
    avatar = scrapy.Field()
    user = scrapy.Field()
    gender = scrapy.Field()
    rank = scrapy.Field()
    regtime = scrapy.Field()
    birthday = scrapy.Field()
    level = scrapy.Field()
    sign = scrapy.Field()
    verify = scrapy.Field()
    follows = scrapy.Field()
    fans = scrapy.Field()
    crawled_at = scrapy.Field()


class BilibiliUserRelationItem(scrapy.Item):
    id = scrapy.Field()
    follows = scrapy.Field()
    fans = scrapy.Field()
    crawled_at = scrapy.Field()


class BilibiliVideoItem(scrapy.Item):
    id = scrapy.Field()
    user = scrapy.Field()
    video = scrapy.Field()
    crawled_at = scrapy.Field()


class BilibiliVideoInfoItem(scrapy.Item):
    id = scrapy.Field()
    user = scrapy.Field()
    tid = scrapy.Field()
    count = scrapy.Field()
    name = scrapy.Field()
    crawled_at = scrapy.Field()

