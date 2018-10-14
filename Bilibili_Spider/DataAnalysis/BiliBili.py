import pymongo
import jieba.posseg as posseg
from collections import Counter
from Bilibili_Spider import settings
from pyecharts import Pie, Line, Bar, WordCloud


class DataAnalysis(object):

    def __init__(self):
        client = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        db = client.Bilibili
        self.collection_user = db.BilibiliUserItem
        self.collection_video = db.BilibiliVideoInfoItem

    def takeFirst(self, elem):
        """对列表数据进行排序"""
        return elem[0]

    def run(self):
        """分析函数主入口"""
        self.gender()
        self.regtime()
        self.vip()
        self.sign()
        self.video_category()
        self.fans()

    def gender(self):
        """bilibili用户性别可视化"""
        print("开始分析：%s" % self.__class__.gender.__name__)
        cursor = self.collection_user.find({}, {"gender": 1, "_id": 0})
        print('数据基数：%s' % cursor.count())
        gender = list(filter(lambda x: len(x) != 0, [gender.get('gender') for gender in cursor]))
        counter = Counter()

        filed, attr = [], []
        for g in gender:
            counter[g] += 1
        for k, v in counter.most_common():
            filed.append(k)
            attr.append(v)

        pie = Pie('BilibiliUser性别分析饼状图')
        pie.add('', filed, attr, is_label_show=True)
        pie.render("gender.html")
        print('Generated a pie chart done!')
        print("分析结束：%s" % self.__class__.gender.__name__)

    def regtime(self):
        """bilibili用户注册年份可视化"""
        print("开始分析：%s" % self.__class__.regtime.__name__)
        cursor = self.collection_user.find({"regtime": {"$ne": None}}, {"regtime": 1, "_id": 0})
        print('数据基数：%s' % cursor.count())
        regtime = [regtime.get('regtime') for regtime in cursor]
        regtime = [t.split('-')[0] for t in regtime]

        counter = Counter()
        filed, attr = [], []
        for t in regtime:
            counter[t] += 1
        rank = counter.most_common()
        rank.sort(key=self.takeFirst)
        for k, v in rank:
            filed.append(k)
            attr.append(v)

        line = Line("Bilibili用户注册时间折线图")
        line.add("Bilibili用户注册时间折线图", filed, attr, is_smooth=True, mark_line=["max", "average"])
        line.render("regtime.html")
        print('Generated a line chart done!')
        print("分析结束：%s" % self.__class__.regtime.__name__)

    def vip(self):
        """bilibili用户会员等级可视化"""
        print("开始分析：%s" % self.__class__.vip.__name__)
        cursor = self.collection_user.find({"level": {"$ne": None}}, {"level": 1, "_id": 0})
        print('数据基数：%s' % cursor.count())
        vip = [vip.get('level') for vip in cursor]
        counter = Counter()
        filed, attr = [], []
        for t in vip:
            counter[t] += 1
        rank = counter.most_common()
        rank.sort(key=self.takeFirst)
        for k, v in rank:
            filed.append(k)
            attr.append(v)

        bar = Bar('BilibiliUser会员等级分析柱状图')
        bar.add('', filed, attr, mark_line=["min", "max"])
        bar.render("vip.html")
        print('Generated a bar chart done!')
        print("分析结束：%s" % self.__class__.vip.__name__)

    def sign(self):
        """分析bilibili用户的签名出现的词频，并且可视化"""
        print("开始分析：%s" % self.__class__.sign.__name__)
        cursor = self.collection_user.find({"sign": {"$ne": None}}, {"sign": 1, "_id": 0})
        print('数据基数：%s' % cursor.count())
        sign = list(filter(lambda x: len(x), [sign.get('sign') for sign in cursor]))
        stop = [line.strip() for line in open('stop_words.txt', 'r', encoding='utf-8').readlines()]  # 加载停用词表
        filed, attr, words = eval("[]," * 3)
        for s in sign:
            segs = posseg.cut(s)
            for seg, flag in segs:
                if seg not in stop:
                    if flag != 'm' and flag != 'x':     # 去数词和去字符串
                        words.append(seg)
        counter = Counter()
        for word in words:
            counter[word] += 1

        for k, v in counter.most_common():
            filed.append(k)
            attr.append(v)

        wordcloud = WordCloud(width=1300, height=620)
        wordcloud.add("", filed, attr, word_size_range=[30, 100], shape='diamond')
        wordcloud.render("sign.html")
        print('Generated a wordclound done!')
        print("分析结束：%s" % self.__class__.sign.__name__)

    def video_category(self):
        """bilibili用户发布的视频分类可视化"""
        print("开始分析：%s" % self.__class__.video_category.__name__)
        cursor = self.collection_video.find({}, {"name": 1, "count": 1, "_id": 0})
        print('数据基数：%s' % cursor.count())
        video_info = [{"name": video.get('name'), "count": video.get('count')} for video in cursor]
        counter = Counter()
        filed, attr = [], []
        for video in video_info:
            counter[video.get('name')] += 1

        for k, v in counter.most_common():
            filed.append(k)
            attr.append(v)

        wordcloud = WordCloud(width=1300, height=620)
        wordcloud.add("", filed, attr, word_size_range=[30, 100], shape='diamond')
        wordcloud.render("category.html")
        print('Generated a wordclound done!')
        print("分析结束：%s" % self.__class__.video_category.__name__)

    def fans(self):
        """粉丝数的分析"""
        print("开始分析：%s" % self.__class__.fans.__name__)
        cursor = self.collection_user.find({}, {"fans": 1, "_id": 0})
        filed = ["无", "个级", "十级", "百级", "千级", "万级", "十万级", "百万级"]
        attr = []
        fans = [fans.get('follower') for fans in cursor]
        no_fans = str(len([f for f in fans if f == "0"]))
        digit = str(len([f for f in fans if len(f) == 1 and f != "0"]))
        tens_digit = str(len([f for f in fans if len(f) == 2]))
        hundred = str(len([f for f in fans if len(f) == 3]))
        thousand = str(len([f for f in fans if len(f) == 4]))
        ten_thousand = str(len([f for f in fans if len(f) == 5]))
        hundred_thousand = str(len([f for f in fans if len(f) == 6]))
        million = str(len([f for f in fans if len(f) == 7]))
        attr.append(no_fans)
        attr.append(digit)
        attr.append(tens_digit)
        attr.append(hundred)
        attr.append(thousand)
        attr.append(ten_thousand)
        attr.append(hundred_thousand)
        attr.append(million)

        bar = Bar('Bilibili用户粉丝数量分析柱状图')
        bar.add('', filed, attr, mark_line=["min", "max"])
        bar.render("fans.html")
        print('Generated a bar chart done!')

        print("分析结束：%s" % self.__class__.fans.__name__)


if __name__ == '__main__':
    analysis = DataAnalysis()
    analysis.run()

