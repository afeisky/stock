#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
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

def readme():
    print("usage: python3 sse.py download download_dir")
    print("       python3 sse.py download begin_date  end_date download_dir")
    print("       python3 sse.py download 2017-08-01  2017-08-31 ./download_szse")
    print("       python3 sse.py input2db ./download_szse")



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
        print("Error: %s download fail!" % filePathName)
        return ""

def download_current_date_sh_data_from_sse_com_cn(subdir):
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #LogOut.write("create_time: %s-----------------\n" % create_time)
    #url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?callback=jQuery111206824883723430116_1501664482387&select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000&_=1501664482391'
    url='http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000'
    #url= 'http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=2000'
    filePathName=os.path.join(subdir,"sse_json.htm")
    print(filePathName)
    filePathName=download_url(url,filePathName,True)
    print(filePathName)
    #LogOut.write("download is  %s\n" % filePathName)
    #copy backup file:
    if not os.path.exists(filePathName):
        print("Error: download fail!")
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
        #LogOut.write("date= %s\n" % date)
        if (a_time>=15):
            need_copy=True
    if need_copy:
        new_file="sse_%s.json"%(d)
        #LogOut.write("copyed!\n")
        print(os.path.join(subdir,new_file))
        shutil.copyfile(filePathName,os.path.join(subdir,new_file))
    #LogOut.close()
    return filePathName


def input2db_from_sse_json(filePathName):
    print(filePathName)
    with codecs.open(filepathname, 'r', 'GB2312') as f:
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
        #sql='select count(*) from inputsha where date_format(date,"%%Y-%%m-%%d")="%s" '%(d)
        #print(sql)
        a_time=int(str(jdata['time'])[:2])
        conn = mysql.connector.connect(user='root', password='chaofei1', host='127.0.0.1', port='3306',
                                       database='afei')
        for idx,line in enumerate(jdata['list']):
            #print(line)
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
            #print(date,',',code,',',name)
            insert_sql = 'insert into in_sse_tmp (date,code,name,last,begin,low,high,price,new,percent,volume,money,gap,wave,peratio,note,data_from,create_time)'
            insert_sql +='values ("%s","%s","%s","%s","%s","%s" , "%s" , "%s", "%s" , "%s", "%s" , "%s" , "%s", "%s" , "%s", "%s" , "%s" , "%s")'
            insert_sql=insert_sql%(date,code,name,last,begin,low,high,price,new,percent,volume,money,gap,wave,peratio,note,data_from,create_time)
            #log("%d,%s"%(idx,insert_sql))
            #Database().execSQL(insert_sql)
            cursor = conn.cursor()
            cursor.execute(insert_sql)
            conn.commit()
            cursor.close()
        conn.close()
        total=0


def main(params):
    print(params)
    if len(params)<2:
        readme()
        exit()
    if params[0]=='download' and len(params) ==2:
        download_dir = params[1]
        if not(download_dir[:1] == '/' or download_dir[1:2] == ':'):
            root_dir = os.getcwd()
            download_dir = os.path.join(root_dir, download_dir)
        if not os.path.exists(download_dir):
            log('Error: not found dir: %s' % download_dir)
            exit(0)
        filePathName = download_current_date_sh_data_from_sse_com_cn(download_dir)
    elif params[0]=='download':
        download_dir = params[4]
        if download_dir[:1] == '/' or download_dir[1:2] == ':':
            root_dir = os.getcwd()
            download_dir = os.path.join(root_dir, download_dir)
        if not os.path.exists(download_dir):
            log('Error: not found dir: %s' % download_dir)
            exit(0)

        begin_date=params[2]
        end_date = params[3]
        #print(begin_date, '->', end_date)
        begin_date1 = time.strptime(begin_date,"%Y-%m-%d")
        end_date1 = time.strptime(end_date, "%Y-%m-%d")
        #begin = datetime.date(2017,7,30)
        #end = datetime.date(2017,7,31)
        begin = datetime.date(begin_date1.tm_year,begin_date1.tm_mon,begin_date1.tm_mday)
        end = datetime.date(end_date1.tm_year,end_date1.tm_mon,end_date1.tm_mday)
        print('download:', begin, '->', end, 'to [' + download_dir + ']')
        #download_sz(begin,end,download_dir)
        filePathName = download_current_date_sh_data_from_sse_com_cn(download_dir)
    elif params[0] == 'input2db':
        download_dir = sys.argv[2]
        if download_dir[:1] == '/' or download_dir[1:2] == ':':
            root_dir = os.getcwd()
            download_dir = os.path.join(root_dir, download_dir)
        if not os.path.exists(download_dir):
            log('Error: not found dir: %s' % download_dir)
            exit(0)
        listdir = os.listdir(download_dir)
        listdir.sort()
        n = 0
        if (len(listdir) > 0):
            fdata = open(os.path.join(os.getcwd(), "sse_out.log"), 'w')
            conn = mysql.connector.connect(user='root', password='chaofei1',
                                           host='127.0.0.1', port='3306', database='afei')
            insert_sql = 'insert into in_sse_tmp (date,code,name,last,price,percent,money,peratio,data_from) values '
            for file in listdir:
                filename = os.path.basename(file)
                print(filename)
                # print(filename)
                # print(filename[:5])
                # print(filename[-4:len(filename)])
                if not (filename[:4] == 'sha_' and filename[-5:len(filename)] == '.json'):
                #if not (filename[:4] == 'sse_' and filename[-5:len(filename)] == '.json'):
                    break
                filepathname = os.path.join(download_dir, filename)
                ret=input2db_from_sse_json(filepathname)
            conn.close()
            fdata.close()


if __name__ == "__main__":
    params=[]
    if sys.argv[1]=='download' and len(sys.argv[1:]) ==2:
        params.append(params[0])
        params.append(params[1])
    elif sys.argv[1]=='download' and len(sys.argv[1:]) ==4:
        params.append(params[0])
        params.append(params[1])
        params.append(params[2])
        params.append(params[3])
    elif sys.argv[1] == 'input2db' and len(params) ==2:
        params.append(params[0])
        params.append(params[1])
    else:
        readme()
    #param = ['download', 'download_sse']
    main(params)


