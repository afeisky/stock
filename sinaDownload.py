#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import datetime
import shutil
import urllib
from urllib import request
import codecs
import mysql
from mysql import connector
import xlrd
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
    #LogOut.write("%s\n"%string)

################

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
    print('download_url=',url)
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
    #time.sleep(2) ##
    try:
        with request.urlopen(url) as web:
            # 为保险起见使用二进制写文件模式，防止编码错误
            with open(filePathName, 'wb') as outfile:
                outfile.write(web.read())
        if (os.path.getsize(filePathName))<3000:  # .获取文件大小, 使用os.path.getsize函数，参数是文件的路径。
            log('download error: delete %s'%filePathName)
            os.remove(filePathName)
            return ''
        else:
            print("download: %s file not exist, need download!"%filePathName)
        return filePathName
    except:
        log('download error: filePathName=%s no data!'%(shotname))
        return ""


def get_url_download_from_sina(code,year,qurter,download_dir):
    filePathName=os.path.join(download_dir,"sina-%s-%d-%d.htm"%(code,year,qurter))
    #url= 'http://www.sse.com.cn/market/price/report/'
    #url='http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/601006.phtml?year=2017&jidu=2'
    url='http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%d&jidu=%d'%(code,year,qurter)
    #print(url)
    #print(filePathName)
    return url,filePathName


def date2year_quarter(code,download_dir):
    d=[{'year':2014,'quarter':[1,2,3,4]},{'year':2015,'quarter':[1,2,3,4]},{'year':2016,'quarter':[1,2,3,4]},{'year':2017,'quarter':[1,2,3]}]
    #d=[{'year':2017,'quarter':[3]}]
    for one in d:
        year=one['year']
        for quarter in one['quarter']:
            filePathName=''
            again=5
            while len(filePathName)==00 and (again>0):
                (url,filePathName)=get_url_download_from_sina(code,year,quarter,download_dir)
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



def parser_json_then_download_history_from_sina(filePathName,download_dir):
    print(filePathName)
    with open(filePathName, 'r') as f:
        jdata = json.load(f)
        #print(data)
        print(len(jdata['list']))
        print(jdata['total'])
        if jdata['total']!=len(jdata['list']):
            print("Error: len(list) != total? ")
        d=str(jdata['date'])
        t=str(jdata['time'])
        print(d,t)
        d='%s-%s-%s'%(d[0:4],d[4:6],d[6:8])
        t='%s:%s:%s'%(t[0:2],t[2:4],t[4:6])
        date="%s %s"%(d,t)
        print(date)
        a_time=int(str(jdata['time'])[:2])
        total=0
        for idx,line in enumerate(jdata['list']):
            code=line[0]
            total+=1
            ret=date2year_quarter(code,download_dir) ###########3
            print(total,"====")
            if (ret==0):
                return

def download_current_date_sh_data_from_sse_com_cn(sse_dir):
    #url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?callback=jQuery111206824883723430116_1501664482387&select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000&_=1501664482391'
    url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000&_=1501664482391'
    filePathName=os.path.join(sse_dir,"sha_now.json.htm")
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
        print(os.path.join(sse_dir,new_file))
        shutil.copyfile(filePathName,os.path.join(sse_dir,new_file))
    return filePathName



def getQuarter(month):
    if month <= 3:
        aquarter = 1
    elif month <= 6:
        aquarter = 2
    elif month <= 9:
        aquarter = 3
    else:
        aquarter = 4
    return aquarter




def szse_read_excel(filename):
    lists = []
    print(filename)
    if not os.path.exists(filename):
        print("Error: %s is not found!" % filename)
        return lists
    workbook = xlrd.open_workbook(filename)

    # sheet
    all_sheets_list = workbook.sheet_names()
    # print("All sheets name in File:",all_sheets_list)

    first_sheet = workbook.sheet_by_index(0)
    # print("First sheet Name:",first_sheet.name)
    print("First sheet Rows:", first_sheet.nrows)
    # print("First sheet Cols:",first_sheet.ncols)

    # first_row=first_sheet.row_values(0)
    # print("First row:",first_row)
    # first_col=first_sheet.col_values(0)
    # print("First Column:",first_col)

    if (first_sheet.nrows < 10):
        return lists

    # print("row0:%s"%first_sheet.row_values(0))
    # print("row0:%s"%first_sheet.row_values(1))
    # print("row0:%s"%first_sheet.row_values(2))

    colDateList = []
    for index, value in enumerate(first_sheet.row_values(0)):
        if ('日期' in value) or ('时间' in value):
            colDateList.append(index)
    print('colDateList=',colDateList)

    try:
        log("%s: rows/cols (%d,%d)" % (filename, first_sheet.nrows, first_sheet.ncols))
        for row in range(1, (first_sheet.nrows)):
            input_date = ''
            input_code = ''
            input_name = ''
            input_last = ''
            input_now = 0
            input_percent = 0
            input_memoy = 0
            input_peraito = 0

            for col in range(0, (first_sheet.ncols)):
                value = first_sheet.cell(row, col).value
                celltype = first_sheet.cell_type(row, col)
                #print("%d,%d : %s"%(row,col,value))
                if (col == 1):
                    #print("1: celltype=%d" % celltype)
                    if celltype == 2:  # is float
                        valueStr = str(value)
                        value = valueStr[:len(valueStr) - 2]
                    #print("%s,%s:%s" % (row, col, value))
                    #print("%d,%d : %s" % (row, col, value))
                    lists.append(value)
        print('len(list)=',len(lists))
        return lists
    except:
        log("[readExcel] Error: %s no data!"%(filename))
        return []
    finally:
        log("[readExcel] %s done."%(filename))
        return lists

def download_sse_and_szse():
    codelist=[]
    retFlag=0

    #url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?callback=jQuery111206824883723430116_1501664482387&select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000&_=1501664482391'
    url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000&_=1501664482391'
    root_dir = os.getcwd()
    filePathName=os.path.join(root_dir,"sse_now.json")
    #print(filePathName)
    if False:
        filePathName=download_url(url,filePathName,True)
        #copy backup file:
        need_copy=False
        with codecs.open(filePathName, 'r', 'GB2312') as f:
            jdata = json.load(f)
            d=str(jdata['date'])
            t=str(jdata['time'])
            print(d,t)
            d='%s-%s-%s'%(d[0:4],d[4:6],d[6:8])
            t='%s:%s:%s'%(t[0:2],t[2:4],t[4:6])
            date="%s %s"%(d,t)
            print(date)
            a_time=int(str(jdata['time'])[:2])
            for idx,line in enumerate(jdata['list']):
                codelist.append(line[0])
            if (a_time>=15):
                need_copy=True
            if need_copy:
                sse_dir=os.path.join(root_dir, '../download/sse')
                new_file = "sse_%s.json" % (d)
                if os.path.exists(sse_dir) and not os.path.exists(os.path.join(sse_dir,new_file)):
                    print(os.path.join(sse_dir, new_file))
                    shutil.copyfile(filePathName,os.path.join(sse_dir,new_file))

    #--szse.cn

    atime = datetime.datetime.now().strftime("%Y-%m-%d")  # '2017-07-20'
    adate = time.strptime(atime, '%Y-%m-%d')
    date1 = datetime.date(adate.tm_year, adate.tm_mon, adate.tm_mday)
    for count in range(10):
        szsefilePathName = os.path.join(root_dir, "szse_now.xlsx")
        print('=====',count)
        add_date = datetime.timedelta(days=count)
        date2 = date1 - add_date
        strDate = date2.strftime("%Y-%m-%d")
        # url = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1815_stock&txtBeginDate=2017-07-21&txtEndDate=2017-07-21&tab1PAGENO=1&ENCODE=1&TABKEY=tab1 HTTP/1.1'
        # file="c:/rd/1.xls"
        url1 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1815_stock&txtBeginDate='
        url2 = '&txtEndDate='
        url3 = '&tab1PAGENO=1&ENCODE=1&TABKEY=tab1'
        url = ("%s%s%s%s%s" % (url1, strDate, url2, strDate, url3))
        #print(url,szsefilePathName)
        #szsefilePathName=download_url(url,szsefilePathName,True)
        #print(szsefilePathName)
        if len(szsefilePathName)>0 and os.path.exists(szsefilePathName):
            retlists=szse_read_excel(szsefilePathName)
            print('len(retlists)=',len(retlists))
            if len(retlists)>0:
                codelist.extend(retlists)
                print('aa  len(codelist)=', len(codelist))
                retFlag=1
                break
            break
    return codelist,retFlag

def main(codelist):
    retFlag=0
    if (len(codelist)==0):
        codelist,retFlag=download_sse_and_szse()
        print('retFlag=',retFlag)
        if not (retFlag==1):
            print("Error: download fail!")
            return(0)
    print('len(codelist)=',len(codelist))
    total=0
    root_dir = os.getcwd()
    sina_file_dir = os.path.join(root_dir, "../download/sina")

    fout1= open(os.path.join(os.getcwd(),"sina_out.log"),'w')

    for idx, code in enumerate(codelist):
        total += 1
        atime = datetime.datetime.now().strftime("%Y-%m-%d")  # '2017-07-20'
        adate = time.strptime(atime, '%Y-%m-%d')
        aquarter = getQuarter(adate.tm_mon)
        date1 = datetime.date(adate.tm_year, adate.tm_mon, adate.tm_mday)

        add_date = datetime.timedelta(days=32)  # datetime.timedelta(days=100)
        date2 = date1 - add_date
        bquarter = getQuarter(date2.month)
        d=[{'year': date1.year, 'quarter': [aquarter]}]
        if not (aquarter==bquarter):
            d.append({'year': date2.year, 'quarter': [bquarter]})
        #---
        d = [{'year': 2014, 'quarter': [1, 2, 3, 4]}, {'year': 2015, 'quarter': [1, 2, 3, 4]},
             {'year': 2016, 'quarter': [1, 2, 3, 4]}, {'year': 2017, 'quarter': [1, 2, 3]}]
        print('d=',d)
        #d = [{'year': 2014, 'quarter': [1, 2, 3, 4]}, {'year': 2015, 'quarter': [1, 2, 3, 4]}]
        for one in d:
            year = one['year']
            for quarter in one['quarter']:
                filePathName = ''
                again = 5
                while len(filePathName) == 0 and (again > 0):
                    (url, filePathName) = get_url_download_from_sina(code, year, quarter,sina_file_dir)
                    fout1.write(url,'  ',filePathName)
                    
                    filePathName = download_url(url, filePathName, False)
                    #print('++',again,' ',filePathName)
                    if len(filePathName) > 0:
                        break
                        again -= 1
                    if len(filePathName) == 00 and (again <= 0):
                        log('Error: exit after try again 5 times! ')
                        #return 0
        print(total, "====")
        if total==len(codelist):
            print("good , OK!")
        #if (ret == 0):
        #    return 0
        fout1.close()

if __name__ == "__main__":
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    root_dir=os.getcwd()
    sse_dir=os.path.join(root_dir,"download/sse")
    filePathName=download_current_date_sh_data_from_sse_com_cn(sse_dir)
    download_file_dir=os.path.join(root_dir,"../download/sina")
    parser_json_then_download_history_from_sina(filePathName,download_file_dir)
    #LogOut.close()
