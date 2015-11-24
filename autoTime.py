#coding:utf-8
__author__ = 'diaoshe'
"获取时间字符串并返回规范化datetime"
import re
import time
import datetime



def strToTime(Timestr):
    "多格式输入 正则表达式进行逻辑匹配,返回统一时间格式"
    if isinstance(Timestr, unicode):
        "统一编码格式"
        Timestr = Timestr.encode('utf-8')







if __name__=="__main__":
    "测试"
    date=['2015年11月18日17:58','6小时前','37分钟前','7小时前','14小时前',u'2015\u5e7411\u670818\u65e515:30 ','2015年11月18日15:39',u'4\u5c0f\u65f6\u524d','3小时前']





    #匹配文本获得匹配结果  无法匹配则返回None
    for each in date:

        if isinstance(each, unicode):
            each = each.encode('utf-8')


        pat1 = r'\d{4}年\d{2}月\d{2}日\d{2}:\d{2}'
        pattern1 = re.compile(pat1)
        match1 = pattern1.match(each)
        print each

        if match1 :

            print 'get年月日！'
            print match1.group()

        else:
            pat2 = r'\d{1,2}小时前'
            pattern2 = re.compile(pat2)
            match2 = pattern2.match(each)
            if match2:
                print 'get小时！'
                print match2.group()

            else:
                pat3 = r'\d{1,2}分钟前'
                pattern3 = re.compile(pat3)
                match3 = pattern3.match(each)
                if match3:
                    print 'get分钟！'
                    print match3.group()
                else:
                    print "呜呜～～"







