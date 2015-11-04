# -×- coding:utf-8-*-
__author__ = 'diaoshe'
from lxml import etree
import re
import requests
import os
import time
from multiprocessing.dummy import Pool as ThreadPool

keyword = '五中全会'
pn = 0
# 新闻/全部

# baidu = 'http://www.baidu.com/s?wd=%s&pn=' % keyword + str(pn)
baidu = 'http://news.baidu.com/ns?word=%s&pn=' % keyword + str(pn)


headers = {

    'Host': 'news.baidu.com',

    'User-Agent': ''

    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
}
def getUrlTime(url):

    # trueUrl = requests.get(url)
    # print trueUrl.url

    # print url
    r = requests.get(url, headers=headers)
    # print r.headers
    #通过捕获错误判断时间
    try:

        return r.headers['Last-Modified']
    except KeyError:
        return r.headers['date']

class baiduNewsSpider(object):
    "找呀找呀找朋友。。。"
    def GetSource(self):
        source = requests.get(baidu)
        if source.status_code == 503: # Why did this happen?
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
        Num = int(round(s / 10)) # Calculation about pages
        print("[+] Results there are %s pages, there are about %s results" % (Num, number))
        Pages = Num * 10 - 10 # Calculation about page number
        return Pages

    def getBox(self,entire):
        selector = etree.HTML(entire)
        box_field = selector.xpath('//div[@class="result"]')
        return box_field

    def GetUrlStrTime(self, obj):

        objitem = {}
        Url = obj.xpath('h3[@class="c-title"]/a/@href')
        Str = obj.xpath('h3[@class="c-title"]/a/text()')
        Time = obj.xpath('p[@class="c-author"]/text()')

        objitem['Url'] = Url
        objitem['Str'] = Str
        objitem['Time'] = Time

        return objitem



if __name__ == "__main__":
    # data['q'] = raw_input('Enter what you want:')
    spider = baiduNewsSpider()
    print("[!] Start run Spider...")
    # text = spider.GetSource() # Get Sources
    Pages = spider.GetPages(spider.GetSource()) # To calculate Pages
    f = open('result.txt', 'a')
    p = 1
    while pn <= Pages:
        print("[+] Start scraping content... The %d page" % p)
        p += 1
        text = spider.GetSource() #获取百度搜索页面数据
        objOfPages = spider.getBox(text)
        print 'ok'
        testobj = spider.GetUrlStrTime(objOfPages[0])
        print testobj
        #多线程分析


        pn = pn + 10
        # 新闻/全部
        # baidu = 'http://www.baidu.com/s?wd=%s&pn=' % keyword + str(pn)
        baidu = 'http://news.baidu.com/ns?word=%s&pn=' % keyword + str(pn)
    #     time.sleep(2) # To prevent Google verification code, dormancy for 30 seconds
    # f.close()