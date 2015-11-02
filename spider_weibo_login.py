# coding:utf-8
__author__ = 'diaoshe'
from lxml import etree
import requests
# 下面的引用可能是不必要的
import sys
# from multiprocessing.dummy import Pool as ThreadPool


# --------函數定義部分------

reload(sys)

sys.setdefaultencoding('utf-8')

'''重新运行前需要删除content.txt文件进行删除，此文件写入采用不删除的累加模式，会导致文件过大'''


# 定义函数

def urllogin(url, id, pwd):
    "模拟登录微博  输入要查看的url 账户 密码  返回登陆后的url"
    url_login = 'https://login.weibo.cn/login/'
    html = requests.get(url).content
    print html
    selector = etree.HTML(html)
    password = selector.xpath('//input[@type="password"]/@name')[0]
    vk = selector.xpath('//input[@name="vk"]/@value')[0]
    action = selector.xpath('//form[@method="post"]/@action')[0]
    print action
    print password
    print vk

    # 提交地址
    new_url = url_login + action

    # 这里注意要使用测试账号，否则会被记录
    data = {
        'mobile': id,
        password: pwd,
        'backURL': url,
        'backTitle': u'微博',
        'tryCount': ' ',
        'vk': vk,
        'submit': u'登录'
    }

    newhtml = requests.post(new_url, data=data).content
    print '登录成功'
    return newhtml


# 定义文件写入
def towrite(contentdict):
    f.writelines(u'发表时间：' + str(contentdict['topic_time']) + '\n')
    f.writelines(u'内容：' + str(contentdict['topic_content']) + '\n')
    f.writelines(u'发帖人：' + str(contentdict['user_name']) + '\n\n')


def spider(html):
    "爬虫"
    selector = etree.HTML(html)
    content_field = selector.xpath('//div[@class="c" and @id]')  # 查找微博中的发言块
    item = {}
    i = 0
    for each in content_field:
        "注意时刻更新爬虫的线索"
        push_time = each.xpath('//span[@class="ct"]/text()')  # 需要进一步处理
        push_info = each.xpath('//span[@class="ctt"]/text()')
        auther = each.xpath('//a[@class="nk"]/text()')

        # 对时间的一点点处理

        print push_time[i][:13]
        print push_info[i]
        print auther[i]

        item['user_name'] = auther[i]
        item['topic_content'] = push_info[i]
        item['topic_time'] = push_time[i][:13]
        towrite(item)  # 写入
        i = i + 1

#定义`登录和爬虫的嵌套函数
def spiderAll(url, id, pwd):
    html = urllogin(url,id,pwd)
    spider(html)

if __name__ == '__main__':
    """ 确定url的构成
   url 为要看的微博地址
   url = 'http://weibo.cn/search/mblog?hideSearchFrame=&keyword=melodyxin28&page=1'
   http://weibo.cn/search/mblog/?

   keyword=melodyxin28&
   advanced=mblog&
   rl=1&
   starttime=20151005&
   endtime=20151006&
   sort=time&
   vt=4"""

    urlhead = 'http://weibo.cn/search/mblog?hideSearchFrame='
    f = open('content.txt', 'a')
    while True:
        ## 接受键盘输入
        keyword = raw_input('Enter the keyword(type \'ctrl + c\' or \'q\' to exit ):')
        if keyword == 'q':
            sys.exit()
        startTime = raw_input('Enter the start time(Format:yyyy-mm-dd):')
        endTime = raw_input('Enter the end time(Format:yyyy-mm-dd):')
        url = urlhead + '&keyword=' + keyword

        if startTime.strip():  # 非空
            url = url + '&starttime=' + startTime
        if endTime.strip():
            url = url + '&endtime=' + endTime  # 登录提权
        print url

        loginurl = urllogin(url, '460373689@qq.com', 'heyuhua199471')
    # 第一次爬取
        spider(loginurl)

    #之后的抓取
        #获取页数

        pageselector = etree.HTML(loginurl)
        maxpage = pageselector.xpath('//input[@name="mp"]/@value')[0]
        maxpage=int(maxpage)+1
        #创建urllist  多线程化
        # pool = ThreadPool(2)
        page = []
        for i in range(2,maxpage):
            newpage = url + '&page=' + str(i)
            page.append(newpage)
            spiderAll(page[i-2],'460373689@qq.com','heyuhua199471')

        # results = pool.map(spiderAll(page,'460373689@qq.com','heyuhua199471'))

        # results = pool.map(spiderAll,page,'460373689@qq.com','heyuhua199471')

        # pool.close()
        f.close()


# 多线程操作在做完google和百度的再说
#    pool = ThreadPool(4)

    # page = []
    # for i in range(1,21):
    #     newpage = 'http://tieba.baidu.com/p/3971950556?pn=' + str(i)
    #     page.append(newpage)
    #
    # results = pool.map(spider, page)
    # pool.close()
    # pool.join()