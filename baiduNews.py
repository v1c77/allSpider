# -×- coding:utf-8-*-
__author__ = 'diaoshe'
from lxml import etree
import re
import requests
import os
import IOmymongo
import autoTime
import datetime
import time
from math import ceil

from multiprocessing.dummy import Pool as ThreadPool

keyword = '习近平@'
pn = 0
# 新闻/全部
baidunews = 'http://news.baidu.com/ns?cl=2&word=%s&pn=' % keyword + str(pn)

# baidunews = 'http://www.baidu.com/s?wd=%s&pn=' % keyword + str(pn)
# baidunews = 'http://news.baidu.com/ns?word=%s&pn=' % keyword + str(pn)

# 精细化时间
starttime = datetime.datetime(2015, 12, 17)     #起始查询时间
oneday = datetime.timedelta(days=1)
stoptime = int(time.mktime(datetime.datetime.now().timetuple()))    #截止时间
str_start_time = int(time.mktime(starttime.timetuple()))
str_end_time = str_start_time + 1798     #一天分成48份

gpc = '&gpc=stf%3D' + str(str_start_time) + '%2C' + str(str_end_time) + '%7Cstftype%3D2'

baidunews = baidunews + gpc
#      &gpc=stf%3D1446307200%2C1448899200%7Cstftype%3D2



# stf = 'stf=' + str(str_start_time) + ',' + str(str_end_time) + '|stftype=2'  # 时间戳

# dates = {       # 传参搜索
#     'ie': 'utf-8',
#     # 'f':'8', ##no
#     # 'rsv_bp':'1',  #no
#     'rsv_idx': '2',  # 一样
#     'tn': '97272809_hao_pg',
#     'wd': keyword,  # 必须
#     'rsv_spt': '1',
#     'oq': keyword,  # 必须
#     # 'rsv_pq':'f45502e700019c1a',   #每次不一样 去掉
#     # 'rsv_t':'d782WhjQfs9J36DrGeC6UejCMJDlygbA/B+c7pmnYlhWKPIuBDnprwiknKCLhdPu70XIFbvb' #不一样
#     # 'rsv_enter':'1'  #no
#     'gpc': stf,  # 时间戳
#     'tfflag': '1'
# }

headers = {

    'Host': 'news.baidu.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate'
}


# def towritetxt(contentdict):
#     "文本存储"
#     f.writelines(u'发表时间：' + str(contentdict['topic_time']) + '\n')
#     f.writelines(u'内容：' + str(contentdict['topic_content']) + '\n')
#     f.writelines(u'发帖人：' + str(contentdict['user_name']) + '\n\n')


def getUrlTime(url):
    # trueUrl = requests.get(url)
    # print trueUrl.url

    # print url
    r = requests.get(url)
    # print r.headers
    # 通过捕获错误判断时间
    try:

        return r.headers['Last-Modified']
    except KeyError:
        return r.headers['date']


class baiduNewsSpider(object):
    "找呀找呀找朋友。。。"

    def GetSource(self):
        source = requests.get(baidunews, headers=headers)
        if source.status_code == 503:  # Why did this happen?
            print("[!] An error occurred! Please check whether any verification code")
            os._exit(0)

        else:
            return source.text

    def GetPages(self, text):
        """ RegEx resultStats, To calculate Pages """

        selector = etree.HTML(text)
        # 新闻
        numstr = selector.xpath('//span[@class="nums"]/text()')[0]

        # numstr = selector.xpath('//div[@class="nums"]/text()')[0]
        # resultStats = re.findall(r"<div id=\"resultStats\">(.*?)<nobr>", text)
        print numstr
        number = filter(str.isalnum, numstr.encode("utf-8"))
        s = float(number)
        Num = int(ceil(s / 10)) + 1  # Calculation about pages
        print("[+] Results there are %s pages, there are about %s results" % (Num, number))
        Pages = Num * 10 -10  # Calculation about page number
        return Pages

    def getBox(self, entire):
        selector = etree.HTML(entire)
        box_field = selector.xpath('//div[@class="result"]')
        return box_field

    def GetUrlStrTime(self, obj):

        objitem = {}
        Url = obj.xpath('h3[@class="c-title"]/a/@href')[0]
        Str = obj.xpath('h3[@class="c-title"]/a//text()')
        Time = obj.xpath('.//p[@class="c-author"]/text()')[0]
        # 字符串的合并处理
        a = ''
        strAll = a.join(Str)

        # 时间的精细化处理
        source = Time.split()[0]
        Time = Time.split()[1:]
        Time = a.join(Time)
        Timeend = autoTime.strToTime(Time)

        objitem['Url'] = Url
        objitem['Str'] = strAll
        objitem['Time'] = Timeend
        objitem['Source'] = source

        return objitem


if __name__ == "__main__":
    # data['q'] = raw_input('Enter what you want:')
    print("[!] Start run  BaiduNewsSpider...")
    spider = baiduNewsSpider()
    mongocont = IOmymongo.conToMogd()

    # bnContion = pymongo.Connection
    # text = spider.GetSource() # Get Sources
    while str_end_time < stoptime:
        print '[+]Start a part spdider'
        p = 1
        pn = 0
        baidunews = 'http://news.baidu.com/ns?cl=2&word=%s&pn=' % keyword + str(pn) + '&gpc=stf%3D' + str(str_start_time) + '%2C' + str(str_end_time) + '%7Cstftype%3D2'
        Pages = spider.GetPages(spider.GetSource())  # To calculate Pages
        while pn <= Pages:
            print("[+] Start scraping content... The %d/%d page" % (p,Pages/10+1                 ))
            p += 1
            text = spider.GetSource()  # 获取百度搜索页面数据
            objOfPages = spider.getBox(text)
            print '[+] Geting source...'

            for each in objOfPages:
                testobj = spider.GetUrlStrTime(each)
                "输出数据"
                print '*url:', testobj['Url'], ',', 'Title:', testobj['Str'], ',', 'Time:', testobj['Time']
                IOmymongo.writeToMongo(mongocont, testobj)

            # 多线程分析

            # 重新加载数据项
            pn = pn + 10

            baidunews = 'http://news.baidu.com/ns?cl=2&word=%s&pn=' % keyword + str(pn) + '&gpc=stf%3D' + str(str_start_time) + '%2C' + str(str_end_time) + '%7Cstftype%3D2'


        #修改精细时间
        str_start_time = str_start_time + 1800
        str_end_time = str_start_time + 1798

        # 新闻/全部

        # baidu = 'http://news.baidu.com/ns?word=%s&rn=50&pn=' % keyword + str(pn)
        #     time.sleep(2) # To prevent Google verification code, dormancy for 30 seconds
        # f.close()
