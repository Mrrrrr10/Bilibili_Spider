# -*- coding: utf-8 -*-
import re
import json
import time
from Bilibili_Spider.items import *
from scrapy.http import Request, FormRequest
from scrapy_redis.spiders import RedisSpider
from Bilibili_Spider.settings import DATE_FORMAT


class BilibiliSpider(RedisSpider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    redis_key = 'bilibili:start_urls'

    space_url = "https://space.bilibili.com/ajax/member/GetInfo"
    relation_url = "https://api.bilibili.com/x/relation/stat?vmid={id}&jsonp=jsonp&callback=__jp7"
    follows_url = "http://api.bilibili.com/x/relation/followings?vmid={id}&pn={pn}&ps=20" \
                  "&order=desc&jsonp=jsonp&callback=__jp6"
    fans_url = "https://api.bilibili.com/x/relation/followers?vmid={id}&pn={pn}&ps=20" \
               "&order=desc&jsonp=jsonp&callback=__jp6"
    videos_url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={id}' \
                 '&pagesize=30&tid=0&page={page}&keyword=&order=pubdate'

    start_uid = ['1532165']
    ids_seen = set()

    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'COOKIES_ENABLED': False,
        'RETRY_TIMES': 10,
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'space.bilibili.com',
            'Referer': 'https://space.bilibili.com',
        }
    }

    formdata = {
        'mid': '',
        'csrf': ''
    }

    def start_requests(self):
        for id in self.start_uid:
            self.formdata.update({
                "mid": str(id)
            })
            yield FormRequest(url=self.space_url, callback=self.parse, formdata=self.formdata, meta={'id': id})

    def parse(self, response):
        """解析用户详细信息"""
        id = response.meta.get('id')
        if id in self.ids_seen:
            self.logger.debug('UserID：%s Already Have Been Crawled!' % id)
        else:
            self.ids_seen.add(id)
            text_json = json.loads(response.text, encoding='utf-8')
            if text_json.get('status'):
                data = text_json.get('data')
                if data:
                    user_item = BilibiliUserItem()
                    filed_map = {
                        "id": "mid", "avatar": "face", "user": "name", "gender": "sex",
                        "regtime": "regtime", "rank": "rank", "birthday": "birthday",
                        "sign": "sign",
                    }
                    for filed, attr in filed_map.items():
                        user_item[filed] = data.get(attr)
                    user_item['level'] = data.get('level_info').get('current_level')
                    user_item['verify'] = data.get('official_verify').get('desc')

                    self.custom_settings.get('DEFAULT_REQUEST_HEADERS').update({
                        'Host': 'api.bilibili.com',
                        'Referer': 'https://space.bilibili.com',
                    })

                    yield Request(
                        url=self.relation_url.format(id=id), callback=self.parse_relation,
                        headers=self.custom_settings.get('DEFAULT_REQUEST_HEADERS'),
                        meta={'user_item': user_item, 'headers': self.custom_settings.get('DEFAULT_REQUEST_HEADERS')}
                    )

    def parse_relation(self, response):
        """解析用户粉丝、关注的数量"""
        user_item = response.meta.get('user_item')
        user_item['follows'] = re.search('"following":(\d+)', response.text).group(1)
        user_item['fans'] = re.search('"follower":(\d+)', response.text).group(1)

        yield user_item

        headers = response.meta.get('headers')

        # 关注
        yield Request(
            url=self.follows_url.format(id=user_item['id'], pn=1),
            callback=self.parse_follows, headers=headers, meta={'headers': headers, 'id': user_item['id'], "pn": 1}
        )

        # 粉丝
        yield Request(
            url=self.fans_url.format(id=user_item['id'], pn=1),
            callback=self.parse_fans, headers=headers, meta={'headers': headers, 'id': user_item['id'], 'pn': 1}
        )

        # 视频
        yield Request(
            url=self.videos_url.format(id=user_item['id'], page=1),
            callback=self.parse_videos, meta={'user': user_item['user'], 'id': user_item['id'], 'pn': 1}
        )

    def parse_follows(self, response):
        """解析用户的关注"""
        text_json = json.loads(response.text.replace('__jp6(', '').replace(')', ''))
        if text_json.get('data').get('list') and not text_json.get('code'):
            data = text_json.get('data')
            follows = data.get('list')
            for follow in follows:
                id = follow.get('mid')
                self.formdata.update({
                    "mid": str(id)
                })
                yield FormRequest(url=self.space_url, callback=self.parse, formdata=self.formdata, meta={'id': id})

            id = response.meta.get('id')

            # 关注列表
            user_relation_item = BilibiliUserRelationItem()
            follows = [{'id': follow.get('mid'), 'user': follow.get('uname')} for follow in follows]
            user_relation_item['id'] = id
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []

            yield user_relation_item

            # 下一页
            headers = response.meta.get('headers')
            pn = response.meta.get('pn') + 1
            yield Request(
                url=self.follows_url.format(id=id, pn=pn),
                callback=self.parse_follows, headers=headers, meta={'headers': headers, 'id': id, 'pn': pn}
            )

    def parse_fans(self, response):
        """解析用户的粉丝"""
        # todo:由于Bilibili官方系统限制了用户查看全部粉丝的限制，只能查看当前用户前5页粉丝，所以也只能抓取用户的前5页粉丝
        text_json = json.loads(response.text.replace('__jp6(', '').replace(')', ''))
        if not text_json.get('code'):
            data = text_json.get('data')
            fans = data.get('list')
            for fan in fans:
                id = fan.get('mid')
                self.formdata.update({
                    "mid": str(id)
                })
                yield FormRequest(url=self.space_url, callback=self.parse, formdata=self.formdata, meta={'id': id})

            id = response.meta.get('id')

            # 粉丝列表
            user_relation_item = BilibiliUserRelationItem()
            fans = [{'id': fan.get('mid'), 'user': fan.get('uname')} for fan in fans]
            user_relation_item['id'] = id
            user_relation_item['fans'] = fans
            user_relation_item['follows'] = []

            yield user_relation_item

            # 下一页
            headers = response.meta.get('headers')
            pn = response.meta.get('pn') + 1
            yield Request(
                url=self.fans_url.format(id=id, pn=pn),
                callback=self.parse_fans, headers=headers, meta={'headers': headers, 'id': id, 'pn': pn}
            )

    def parse_videos(self, response):
        """解析用户发布的视频"""
        text_json = json.loads(response.text)
        if text_json.get('status'):
            data = text_json.get('data')
            if data and len(data.get('tlist')) and len(data.get('vlist')):
                video_info_item = BilibiliVideoInfoItem()
                tlist = data.get('tlist')
                id = response.meta.get('id')
                user = response.meta.get('user')
                for filed, attr in tlist.items():
                    for f, a in attr.items():
                        video_info_item[f] = a
                    video_info_item['id'] = id
                    video_info_item['user'] = user

                    yield video_info_item

                video_item = BilibiliVideoItem()
                vlist = data.get('vlist')
                video = [{
                    'aid': video.get('aid'),
                    'author': video.get('author'),
                    'title': video.get('title'),
                    'desc': video.get('description'),
                    'created': time.strftime(DATE_FORMAT, time.localtime(float(video.get('created')))),
                    'typeid': video.get('typeid'),
                    'length': str(int(video.get('length').split(":")[0]) * 60 + int(video.get('length').split(":")[1])),
                    'comment': video.get('comment'),
                    'play': video.get('play'),
                    'review': video.get('video_review'),
                    'favorites': video.get('favorites')
                } for video in vlist]

                video_item['id'] = id
                video_item['user'] = user
                video_item['video'] = video

                yield video_item

                # 下一页
                pn = response.meta.get('pn') + 1
                yield Request(
                    url=self.videos_url.format(id=id, page=pn),
                    callback=self.parse_videos, meta={'user': user, 'id': id, 'pn': pn}
                )
