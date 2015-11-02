# -×- coding:utf-8-*-
__author__ = 'diaoshe'
from lxml import etree
import re
import requests
import os
import time

keyword = '赵日天'

baidu = 'http://www.baidu.com/s?wd=%s&pn=' % keyword


def getUrlTime(url):
    r = requests.get(url)
    return r.headers['last-modified']

class baiduSpider(object):
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
        numstr = selector.xpath('//div[@class="nums"]/text()')[0]
        # resultStats = re.findall(r"<div id=\"resultStats\">(.*?)<nobr>", text)
        print numstr
        number = filter(str.isalnum, numstr.encode("utf-8"))
        s = float(number)
        Num = int(round(s / 10)) # Calculation about pages
        print("[+] Results there are %s pages, there are about %s results" % (Num, number))
        Pages = Num * 10 - 10 # Calculation about page number
        return Pages

    def GetUrl(self, start):
        # Url = re.findall(r"<h3 class=\"t\"><a href=\"(.*?)\" target=\"_blank", start)
        selector = etree.HTML(start)
        Url = selector.xpath('//h3[@class="t"]/a/@href')

        return Url



if __name__ == "__main__":
    # data['q'] = raw_input('Enter what you want:')
    spider = baiduSpider()
    pn = 0
    print("[!] Start run Spider...")
    text = spider.GetSource() # Get Sources
    Pages = spider.GetPages(text) # To calculate Pages
    f = open('result.txt', 'a')
    p = 1
    while pn <= Pages:
        print("[+] Start scraping content... The %d page" % p)
        p += 1
        text = spider.GetSource()
        for i in spider.GetUrl(text):
            f.writelines(i + '\n')
            print i
            urltime = getUrlTime(i)
            print urltime
        pn = pn + 10
    #     time.sleep(2) # To prevent Google verification code, dormancy for 30 seconds
    # f.close()