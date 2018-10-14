# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import pymongo
from Bilibili_Spider.items import *
from Bilibili_Spider.settings import *


class BilibiliSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


# ---------- Bilibili_Pipeline ----------
class Bilibili_Pipeline():
    def process_item(self, item, spider):
        if isinstance(item, BilibiliUserItem):
            if item.get('regtime'):
                item['regtime'] = time.strftime(DATE_FORMAT, time.localtime(float(item['regtime'])))

            if item.get('sign'):
                item['sign'] = item['sign'].strip()

        return item


# ---------- Time_Pipeline ----------
class TimePipeline():
    def process_item(self, item, spider):
        now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item['crawled_at'] = now

        return item


# ---------- MongoDB_Pipeline ----------
class MongoPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGODB_HOST'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_db=crawler.settings.get('MONGODB_DBNAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, BilibiliUserItem) or isinstance(item, BilibiliVideoInfoItem):
            self.db[item.__class__.__name__].create_index([('id', pymongo.ASCENDING)])
            self.db[item.__class__.__name__].update({'id': item.get('id')}, {'$set': item}, True)

        if isinstance(item, BilibiliUserRelationItem):
            self.db[item.__class__.__name__].update(
                {'id': item.get('id')},
                {'$addToSet':
                    {
                        'follows': {'$each': item['follows']},
                        'fans': {'$each': item['fans']}
                    }
                }, True)

        if isinstance(item, BilibiliVideoItem):
            self.db[item.__class__.__name__].update(
                {'id': item.get('id')},
                {'$addToSet':
                     {
                         'video': {'$each': item['video']}
                     }

                }, True)

        return item
