#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import datetime
import shutil
import codecs
import urllib
from urllib import request
import mysql
from mysql import connector
import xlrd
#from html2json import html2json
from bs4 import BeautifulSoup

def log(string):
    #global LogOut
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    if ('Error:' in string) or ('ERROR:' in string):
         print("\033[31;1m %s\033[0m"%string)
    else:
        print("%s\n"%string)
    #LogOut.write("%s\n"%string)
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

def download_current_date_sh_data_from_sse_com_cn():
    LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LogOut.write("create_time: %s-----------------\n" % create_time)
    #url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?callback=jQuery111206824883723430116_1501664482387&select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000&_=1501664482391'
    url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000'
    #url= 'http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000'
    root_dir=os.getcwd()
    download_file_dir=os.path.join(root_dir,"download")
    subdir=os.path.join(download_file_dir,"sha")
    filePathName=os.path.join(subdir,"sha_now.json.htm")
    print(filePathName)
    filePathName=download_url(url,filePathName,True)
    print(filePathName)
    LogOut.write("download is  %s\n" % filePathName)
    #copy backup file:
    need_copy=False
    with codecs.open(filePathName,'r','GB2312') as f:
        jdata = json.load(f)
        d=str(jdata['date'])
        t=str(jdata['time'])
        print(d,t)
        d='%s-%s-%s'%(d[0:4],d[4:6],d[6:8])
        t='%s:%s:%s'%(t[0:2],t[2:4],t[4:6])
        date="%s %s"%(d,t)
        print(date)
        a_time=int(str(jdata['time'])[:2])
        LogOut.write("date= %s\n" % date)
        if (a_time>=15):
            need_copy=True
    if need_copy:
        new_file="sha_%s.json"%(d)
        LogOut.write("copyed!\n")
        print(os.path.join(subdir,new_file))
        shutil.copyfile(filePathName,os.path.join(subdir,new_file))
    LogOut.close()
    return filePathName

if __name__ == "__main__":
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    filePathName=download_current_date_sh_data_from_sse_com_cn()
    #LogOut.close()
