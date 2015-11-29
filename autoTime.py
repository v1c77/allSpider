#coding:utf-8
__author__ = 'diaoshe'
"获取时间字符串并返回规范化datetime"
import re
import time
import datetime

now = datetime.datetime.now()

def strToTime(Timestr):
    "多格式输入 正则表达式进行逻辑匹配,返回统一时间格式"
    if isinstance(Timestr, unicode):
        "统一编码格式"
        Timestr = Timestr.encode('utf-8')
        pat1 = r'\d{4}年\d{2}月\d{2}日\d{2}:\d{2}'
        pattern1 = re.compile(pat1)
        match1 = pattern1.match(Timestr)


        if match1 :


            unifidtime = datetime.datetime.strptime(Timestr,'%Y年%m月%d日%H:%M')
            return unifidtime
        else:
            pat2 = r'(\d{1,2})小时前'
            pattern2 = re.compile(pat2)
            match2 = pattern2.match(Timestr)
            if match2:

                hourstr = int(match2.group(1))
                hour = datetime.timedelta(hours=hourstr)
                unifidtime = now - hour
                return unifidtime


            else:
                pat3 = r'(\d{1,2})分钟前'
                pattern3 = re.compile(pat3)
                match3 = pattern3.match(Timestr)
                if match3:

                    minstr = int(match3.group(1))
                    minutes = datetime.timedelta(minutes=minstr)
                    unifidtime = now - minutes
                    return unifidtime
                else:
                    print "呜呜~没有找到~"







if __name__=="__main__":
    "测试"
    date=['2015年11月18日17:58','6小时前','37分钟前','7小时前','14小时前',u'2015\u5e7411\u670818\u65e515:30','2015年11月18日15:39',u'4\u5c0f\u65f6\u524d','3小时前']
    print '现在时间',now




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
            unifidtime = datetime.datetime.strptime(each,'%Y年%m月%d日%H:%M')
            print unifidtime
        else:
            pat2 = r'(\d{1,2})小时前'
            pattern2 = re.compile(pat2)
            match2 = pattern2.match(each)
            if match2:
                print 'get小时！'
                hourstr = int(match2.group(1))
                hour = datetime.timedelta(hours=hourstr)
                unifidtime = now - hour
                print unifidtime


            else:
                pat3 = r'(\d{1,2})分钟前'
                pattern3 = re.compile(pat3)
                match3 = pattern3.match(each)
                if match3:
                    print 'get分钟！'
                    minstr = int(match3.group(1))
                    minutes = datetime.timedelta(minutes=minstr)
                    unifidtime = now - minutes
                    print unifidtime
                else:
                    print "呜呜～～"







