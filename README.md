# Bilibili_Spider
**基于scrapy-redis的分布式爬虫**
## 说明：
1. 爬取Bilibili用户信息及该用户发布的视频信息
2. 存储在mongodb，并且利用mongodb相关api在pipeline.py文件进行数据去重和增量更新
3. 额外增加了布隆过滤器
4. 对爬取的数据进行数据清洗、分析、可视化操作
## 安装：
```
pip install scrapy
pip install scrapy-redis-bloomfilter 
```
## 用法：
```
scrapy crawl bilibili
```
## 数据分析、可视化：
1. 视频分类词云图
![Result1](https://github.com/Mrrrrr10/Bilibili_Spider/blob/master/Bilibili_Spider/DataAnalysis/category.png)
2. 粉丝
![Result1](https://github.com/Mrrrrr10/Bilibili_Spider/blob/master/Bilibili_Spider/DataAnalysis/fans.png)
3. 性别
![Result1](https://github.com/Mrrrrr10/Bilibili_Spider/blob/master/Bilibili_Spider/DataAnalysis/gender.png)
4. 注册时间
![Result1](https://github.com/Mrrrrr10/Bilibili_Spider/blob/master/Bilibili_Spider/DataAnalysis/regetime.png)
5. 签名词频
![Result1](https://github.com/Mrrrrr10/Bilibili_Spider/blob/master/Bilibili_Spider/DataAnalysis/sign.png)
6. 会员等级
![Result1](https://github.com/Mrrrrr10/Bilibili_Spider/blob/master/Bilibili_Spider/DataAnalysis/vip.png)

## 即将进行：
1. 支持视频下载
2. 对视频信息进行详细的分析
