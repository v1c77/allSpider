#!/usr/bin/ python
#coding: utf-8
__times__ = '2015-10-29'
__author__ = 'diaoshe'

from lxml import etree
import os
import requests

import re
import time

Google = "https://www.google.co.jp/search"
data = {
    'q': '五中全会',
    'newwindo': '1',
    'hl': 'zh',
    'biw': '1920',
    'bin': '709',
    'noj': '1',
    'ei': '6IfVVY-aFse30gTY07zAAQ',
    'start': 0,
    'sa': 'N'
}
headers = {
    'host': 'www.google.co.jp',
    'method': 'GET',
    'referer': 'www.google.co.jp/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
}

proxies = {
    "http": "http://128.199.200.205:3128"
}
def getUrlTime(url):
    r = requests.get(url, proxies=proxies)
    return r.headers['last-modified']


class spider(object):
    def GetSource(self):
        """ HTTP Get Google HTML Sources """
        # myproxy = requests.Session()
        # proxy = {
        #     'http': 'http://127.0.0.1:1080',
        #     'https': 'http://127.0.0.1:1080'
        # }
        #
        # Source = myproxy.get(Google, params=data, headers=headers, proxies=proxy, verify=False)
        # 添加代理模块
        Source = requests.get(Google, params=data, headers=headers)
        if Source.status_code == 503: # Why did this happen?
            print("[!] An error occurred! Please check whether any verification code")
            os._exit(0)
        else:
            return Source.text

    def GetPages(self, text):
        """ RegEx resultStats, To calculate Pages """
        resultStats = re.findall(r"<div id=\"resultStats\">(.*?)<nobr>", text)
        number = re.findall(r" (.*?) ", str(resultStats))
        s = float(number[0].replace(",",""))
        Num = int(round(s / 10)) # Calculation about pages
        print("[+] Results there are %s pages, there are about %s results" % (Num, number[0]))
        Pages = Num * 10 - 10 # Calculation about page number
        return Pages

    def GetUrl(self, start):
        """ Grab a links """
        Url = re.findall(r"<h3 class=\"r\"><a href=\"(.*?)\" onmousedown=\"return rwt", start)
        return Url

if __name__ == "__main__":
    # data['q'] = raw_input('Enter what you want:')
    spider = spider()
    print("[!] Start run Spider...")
    text = spider.GetSource() # Get Sources
    Pages = spider.GetPages(text) # To calculate Pages
    f = open('result.txt', 'a')
    p = 1
    while data['start'] <= Pages:
        print("[+] Start scraping content... The %d page" % p)
        p += 1
        text = spider.GetSource()
        for i in spider.GetUrl(text):
            f.writelines(i + '\n')
            print  i
            urltime = getUrlTime(i)
            print urltime
        data['start'] = data['start'] + 10
        time.sleep(2) # To prevent Google verification code, dormancy for 30 seconds
    f.close()
