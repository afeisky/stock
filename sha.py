#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import datetime
import shutil
import urllib
from urllib import request
import mysql
from mysql import connector
import xlrd
#from html2json import html2json
from bs4 import BeautifulSoup

__DONNOT_DOWNLOAD_EXIST_FILE=1

global LogOut

##pip3 install xlrd


def log(string):
    global LogOut
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    if ('Error:' in string) or ('ERROR:' in string):
         print("\033[31;1m %s\033[0m"%string)
    else:
        print("%s\n"%string)
    LogOut.write("%s\n"%string)

def zxb_download(date,filePathName):
    #url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/601006.phtml?year=2017&jidu=2'
    #file="f:/rd/1.xls"
    if __DONNOT_DOWNLOAD_EXIST_FILE and os.path.exists(filePathName):
        return
    url1= 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/601006.phtml?year=2017&jidu=2'
    url2='&jidu='
    year=2017
    quarter=2
    url=("%s%d%s%d"%(url1,year,url2,quarter))
    print(url)
    print(filePathName)
    url = url.encode("utf-8")
    with request.urlopen(url) as web:
        html=web.read()
        # 为保险起见使用二进制写文件模式，防止编码错误
        with open(filePathName, 'wb') as outfile:
            outfile.write(html)




################


def download_all(from_date,to_date):
    begin = datetime.date(2017,1,1)
    end = datetime.date(2017,1,1)

    root_dir=os.getcwd()
    #root_dir='f:\\rd'
    download_file_dir=os.path.join(root_dir,"download")
    print("--> go")
    d = begin
    delta = datetime.timedelta(days=1)
    zxbDir=os.path.join(download_file_dir,"sina")
    if not os.path.exists(zxbDir):
        os.makedirs(zxbDir)
    if not os.path.exists(zxbDir):
        print("Error: %s is not found!"%zxbDir)
    else:
        while d <= end:
            zxb_download(d.strftime("%Y-%m-%d"),os.path.join(zxbDir,d.strftime("%Y-%m-%d.html")))

            #fileName=d.strftime("zxb_%Y-%m-%d.xls")
            #print(file_name)
            #print(d.strftime("%Y-%m-%d"))
            ##########
            #zxb:
            #zxbFilePathName=os.path.join(zxbDir,fileName)
            #if not os.path.exists(zxbFilePathName):
                #print("Error: %s is not found!"%filePathName)
               #zxb_download(d.strftime("%Y-%m-%d"),zxbFilePathName)
            #zb:

            ##########
            d += delta
#################
#download_all("2017-7-21",'2017-7-21')


'''

def download_sh_from_sina(code,year,qurter):
    root_dir=os.getcwd()
    #root_dir='f:\\rd'
    download_file_dir=os.path.join(root_dir,"download")
    subdir=os.path.join(download_file_dir,"sina")
    #filePathName=os.path.join(subdir,"sina.htm")
    filePathName=os.path.join(subdir,"sina-%s-%d-%d.htm"%(code,year,qurter))
    #url= 'http://www.sse.com.cn/market/price/report/'
    #url='http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/601006.phtml?year=2017&jidu=2'
    url='http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%d&jidu=%d'%(code,year,qurter)
    print(url)
    print(filePathName)
    if os.path.exists(filePathName):
        print("Warnning: %s exist!"%filePathName)
        return filePathName
    #url = url.encode("utf-8")
    try:
        with request.urlopen(url) as web:
            # 为保险起见使用二进制写文件模式，防止编码错误
            with open(filePathName, 'wb') as outfile:
                outfile.write(web.read())
        #if ()
        return filePathName
    except:
        log('[readExcel] Error: code=%s year=%d,jidu=%d no data!'%(code,year,qurter))
        return ""

'''

def download_url(url,filePathName,downloadExists=False):
    print(url)
    print(filePathName)
    (filepath,tempfilename) = os.path.split(filePathName);
    (shotname,extension) = os.path.splitext(tempfilename);
    if os.path.exists(filePathName) and (os.path.getsize(filePathName)) < 3000:  # .获取文件大小, 使用os.path.getsize函数，参数是文件的路径。
        log('Error: delete %s' % filePathName)
        os.remove(filePathName)
    if (not downloadExists) and os.path.exists(filePathName):
        print("Warnning: %s file exist, donnot download!"%filePathName)
        return filePathName
    #url = url.encode("utf-8")
    time.sleep(1) ##
    try:
        with request.urlopen(url) as web:
            # 为保险起见使用二进制写文件模式，防止编码错误
            with open(filePathName, 'wb') as outfile:
                outfile.write(web.read())
        if (os.path.getsize(filePathName))<3000:  # .获取文件大小, 使用os.path.getsize函数，参数是文件的路径。
            log('Error: delete %s'%filePathName)
            os.remove(filePathName)
            return ''
        else:
            print("====> %s file not exist, need download!"%filePathName)
        return filePathName
    except:
        log('[readExcel] Error: filePathName=%s no data!'%(shotname))
        return ""


def get_url_download_from_sina(code,year,qurter):
    root_dir=os.getcwd()
    #root_dir='f:\\rd'
    download_file_dir=os.path.join(root_dir,"download")
    subdir=os.path.join(download_file_dir,"sina")
    #filePathName=os.path.join(subdir,"sina.htm")
    filePathName=os.path.join(subdir,"sina-%s-%d-%d.htm"%(code,year,qurter))
    #url= 'http://www.sse.com.cn/market/price/report/'
    #url='http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/601006.phtml?year=2017&jidu=2'
    url='http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%d&jidu=%d'%(code,year,qurter)
    print(url)
    print(filePathName)
    return url,filePathName

def parser_excel_from_sina(filepathname):
    '''
    root_dir=os.getcwd()
    #root_dir='f:\\rd'
    download_file_dir=os.path.join(root_dir,"download")
    subdir=os.path.join(download_file_dir,"sha")
    filepathname=os.path.join(subdir,"sina.htm")
    '''
    if os.path.isfile(filepathname) and os.path.exists(filepathname):
        fileHandle = open(filepathname)
        fileList=fileHandle.readlines()
        fileHandle.close()
        #print(fileList)
        content=""
        find=False
        for fileLine in fileList:
            #print(n,",",fileLine)
            if  find:
                content+=fileLine
            if "历史交易begin" in fileLine:
                find=True
            if "历史交易end" in fileLine:
                break
        #print(content)
        soup = BeautifulSoup(content, 'html.parser')
        #print(soup.prettify())
        #table=soup.find(id="FundHoldSharesTable")
        table = soup.find("table", {"id":"FundHoldSharesTable"})
        #print(table.prettify())
        head=table.findAll('th')
        #print(table.findAll('th'))

        thTag=table.th #th=table.find('th') #th=table.find("th", class_="head")
        #print(thTag)
        #print(thTag.name)
        #print(thTag.attrs)
        #print(thTag.contents)
        #print(thTag.contents[0].replace('\t','').replace('\n',''))
        str=thTag.contents[0].replace('\t','').replace('\n','')
        pos1=str.find('(')
        pos2=str.find(')')
        #print(pos1,'\n',pos2)
        name=str[0:pos1]
        code=str[pos1+1:pos2]
        print(name,code)

        data_list = []
        #for tr in table.findAll('tr'):
        find=False
        for index, tr in enumerate(soup.findAll('tr')):
            tds = tr.findAll("td")
            #print(tds)

            if (len(tds)>0):
                print("+++",tds[0].contents[0])
                rows=[]
                for idx,td in enumerate(tds):
                    #lines.append(td.getText())
                    str=td.getText().replace('\t','').replace('\n','')
                    print(str)
                    rows.append(str)
                    print(idx,"=",td.getText())

                print(rows)
                #print(td.find(text=True))
            if ('日期' in rows[0]):
                find=True
                continue
            if find:
                data_list.append(rows)
        print(data_list)
        if (not find):
            return 0
#        2017-08-02  13.440 13.600 13.440 13.390 61644148 830433621

        for line in data_list:
            print(line)
            date=line[0]
            begin=line[1]
            high=line[2]
            price=line[3]
            low=line[4]
            volume=line[5]
            money=line[6]
            #----
            data_from='sina' #
            create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(date,',',code,',',name)
            insert_sql = 'insert into inputsina (date,code,name,begin,low,high,price,volume,money,data_from,create_time)'
            insert_sql +='values ("%s","%s","%s","%s","%s","%s" , "%s" , "%s", "%s", "%s", "%s")'
            insert_sql=insert_sql%(date,code,name,begin,low,high,price,volume,money,data_from,create_time)
            log("%d,%s"%(idx,insert_sql))
            Database().execSQL(insert_sql)
        return len(data_list)

class Database():
    conn =None
    def __init__(self):
        conn = mysql.connector.connect(user='chaofei', password='chaofei1',host='127.0.0.1',port='3307',database='chaofei')
        pass

    def getTableCount(self,sql):
        cursor = self.conn.cursor()
        #print(sql)
        cursor.execute(sql)
        cities = cursor.fetchall()
        #print(cities)
        #print(cities[0][0])
        return cities[0][0]

    def countThisDate(self,strDate):
        sql='SELECT COUNT(*) FROM input WHERE date="%s"'%(strDate)
        count=self.getTableCount(self,sql)
        print("%d,%s"%(count,sql))
        return count

    def countThisDate(self,strDate):
        sql='SELECT COUNT(*) FROM input WHERE date="%s"'%(strDate)
        count=self.getTableCount(self,sql)
        print("%d,%s"%(count,sql))
        return count

    def execSQL(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()


def date2year_quarter(code):
    d=[{'year':2014,'quarter':[1,2,3,4]},{'year':2015,'quarter':[1,2,3,4]},{'year':2016,'quarter':[1,2,3,4]},{'year':2017,'quarter':[1,2,3]}]
    #d=[{'year':2017,'quarter':[3]}]
    for one in d:
        year=one['year']
        for quarter in one['quarter']:
            filePathName=''
            again=5
            while len(filePathName)==00 and (again>0):
                (url,filePathName)=get_url_download_from_sina(code,year,quarter)
                filePathName=download_url(url,filePathName,False)
                if len(filePathName)>0:
                    break
                    #if parser_excel_from_sina(filePathName)==0:
                    #    return 0
                    #else:
                    #    break
                again-=1
            if len(filePathName)==00 and (again<=0):
                log('Error: exit after try again 5 times! ')
                return 0



def parser_json_then_download_history_from_sina(filePathName):
    print(filePathName)
    with open(filePathName, 'r') as f:
        jdata = json.load(f)
        #print(data)
        print(len(jdata['list']))
        print(jdata['total'])
        if jdata['total']!=len(jdata['list']):
            print("Error: len(list) != total? ")
        #insert_sql = 'insert into inputsha (date,code,name,last,begin,price,new,percent,money,peratio,data_from,create_time)'
        #insert_sql +='values ("%s" , "%s" ,"%s" , "%s" , "%s" , "%s" , "%s" , "%s", "%s" , "%s")'
        #insert_sql=insert_sql%(input_date,input_code,input_name,input_last,input_now,input_percent,input_memoy,input_peraito,"www.szse.cn",create_time)
        #log(insert_sql)
#{"date":20170803,"time":151107,"total":1361,"begin":0,"end":1361,"list":[
#        0      1       2开   3开   4高   5低  6前收   7涨跌幅  8手     9万元        10     11涨跌值  12振幅
# ["600000","浦发银行",13.42,13.42,13.04,13.08,13.44,-2.68,    78581867,1036842141, "E111",   -0.36,   2.83]
        # 开，高，低，振幅 ，手，万无
        d=str(jdata['date'])
        t=str(jdata['time'])
        print(d,t)
        d='%s-%s-%s'%(d[0:4],d[4:6],d[6:8])
        t='%s:%s:%s'%(t[0:2],t[2:4],t[4:6])
        date="%s %s"%(d,t)
        print(date)
        sql='select count(*) from inputsha where date_format(date,"%%Y-%%m-%%d")="%s" '%(d)
        print(sql)
        a_time=int(str(jdata['time'])[:2])
        if False:
            if (Database().getTableCount(sql)==0) and (a_time>=15):
                for idx,line in enumerate(jdata['list']):
                    print(line)
                    code=line[0]
                    name=line[1]
                    begin=line[2]
                    high=line[3]
                    low=line[4]
                    new=0
                    price=0
                    if (a_time>=15): #收盘后的数据
                        new=0   #最新  time: maybe 14:11:13
                        price=line[5]   #当日    time ='151107' , >15:00:00
                    else:
                        new=line[5]   #最新  time: maybe 14:11:13
                        price=0   #当日    time ='151107' , >15:00:00
                    last=line[6]
                    percent=line[7]  #涨跌幅
                    volume=line[8]   #成交量(手)
                    money=line[9]   #成交额(万元)
                    note=line[10]  #上海标识   E111, T111
                    gap=line[11]   #涨跌值
                    wave=line[12] #振幅
                    peratio=0   #市盈率
                    data_from='www.sse.com.cn' #
                    create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(date,',',code,',',name)
                    insert_sql = 'insert into inputsha (date,code,name,last,begin,low,high,price,new,percent,volume,money,gap,wave,peratio,note,data_from,create_time)'
                    insert_sql +='values ("%s","%s","%s","%s","%s","%s" , "%s" , "%s", "%s" , "%s", "%s" , "%s" , "%s", "%s" , "%s", "%s" , "%s" , "%s")'
                    insert_sql=insert_sql%(date,code,name,last,begin,low,high,price,new,percent,volume,money,gap,wave,peratio,note,data_from,create_time)
                    log("%d,%s"%(idx,insert_sql))
                    Database().execSQL(insert_sql)
        total=0
        for idx,line in enumerate(jdata['list']):
            code=line[0]
            total+=1
            ret=date2year_quarter(code)
            print(total,"====")
            if (ret==0):
                return



def download_current_date_sh_data_from_sse_com_cn():
    #url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?callback=jQuery111206824883723430116_1501664482387&select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000&_=1501664482391'
    url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000&_=1501664482391'
    root_dir=os.getcwd()
    download_file_dir=os.path.join(root_dir,"download")
    subdir=os.path.join(download_file_dir,"sha")
    filePathName=os.path.join(subdir,"sha_now.json.htm")
    print(filePathName)
    #filePathName=download_url(url,filePathName,True)
    print(filePathName)
    #copy backup file:
    need_copy=False
    with open(filePathName, 'r') as f:
        jdata = json.load(f)
        d=str(jdata['date'])
        t=str(jdata['time'])
        print(d,t)
        d='%s-%s-%s'%(d[0:4],d[4:6],d[6:8])
        t='%s:%s:%s'%(t[0:2],t[2:4],t[4:6])
        date="%s %s"%(d,t)
        print(date)
        a_time=int(str(jdata['time'])[:2])
        if (a_time>=15):
            need_copy=True
    if need_copy:
        new_file="sha_%s.json"%(d)
        print(os.path.join(subdir,new_file))
        shutil.copyfile(filePathName,os.path.join(subdir,new_file))
    return filePathName

if __name__ == "__main__":
    LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    filePathName=download_current_date_sh_data_from_sse_com_cn()
    parser_json_then_download_history_from_sina(filePathName)
    LogOut.close()
'''
    return
def aaa():

    th=th.replace('\t','').replace('\n','')
    pos1=th.find('>')
    pos2=th.find('<')
    print(pos1,',',pos2)
    #th=table.findAll("thead") #.find(text=True)
    strName=strName.replace('\t','').replace('\n','')
    pos1=strName.find('>')
    pos2=strName.find('<')
    print(pos1,',',pos2)
'''
