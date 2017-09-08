#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import datetime
import shutil
import urllib
from urllib import request
import mysql
from mysql import connector
import xlrd
import codecs
import shutil
#from html2json import html2json

from bs4 import BeautifulSoup

__DONNOT_DOWNLOAD_EXIST_FILE=1

global LogOut

##pip3 install xlrd

def readme():
    print('Usage:\n' +
          '  python3 sinaParse.py {from_sina_html_DIR} {to_sina_data_DIR} \n'+
          '  python3 sinaParse.py "c:\\download\sina"  "c:\\download\sina_data" \n'+
          '  python3 sinaParse.py\n'+
          '  python3 sinaParse.py "/disk1/download/sina/sina-600830-2017-1.htm" "/disk1/download/sina_data/sina-600830-2017-1.htm"'
         )

def log(string):
    #global LogOut
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    if ('Error:' in string) or ('ERROR:' in string):
         print("\033[31;1m %s\033[0m"%string)
    else:
        print("%s\n"%string)
    #LogOut.write("%s\n"%string)
'''
def parse_sina_data1(subdir,filename,sinadata_subdir):
    filepathname = os.path.join(subdir, filename)
    if (len(filepathname) > 0):
        farray = filename.split('-')
        code = farray[1]
        (code, name, data_list) = parser_html_from_sina(filepathname)
        print(code, name, data_list)


def filecopy(filePathName):
    root_dir = os.getcwd()
    download_file_dir = os.path.join(root_dir, "download")
    #subdir1 = os.path.join(download_file_dir, "sina9")
    #shutil.copyfile(filePathName, os.path.join(subdir1, 'sina-603738-2016-1.htm'))
'''
def parser_html_from_sina(filepathname):
    '''
    root_dir=os.getcwd()
    #root_dir='f:\\rd'
    download_file_dir=os.path.join(root_dir,"download")
    subdir=os.path.join(download_file_dir,"sha")
    filepathname=os.path.join(subdir,"sina.htm")
    '''
    data_list = []
    code=0
    name=''
    find = False
    findEnd = False
    if os.path.isfile(filepathname) and os.path.exists(filepathname):
        fileHandle = codecs.open(filepathname, 'r', 'GB2312')#fileHandle = open(filepathname)
        fileList=fileHandle.readlines()
        fileHandle.close()
        #print(fileList)
        content=""
        for fileLine in fileList:
            #print(n,",",fileLine)
            if  find:
                content+=fileLine
            if "历史交易begin" in fileLine:
                find=True
            if "历史交易end" in fileLine:
                findEnd=True
                break
        if not(find and findEnd):
            return code, name, data_list

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
        name=str[0:pos1].strip()
        code=str[pos1+1:pos2].strip()
        #print(name,code)


        #for tr in table.findAll('tr'):
        find=False
        for index, tr in enumerate(soup.findAll('tr')):
            tds = tr.findAll("td")
            #print(tds)

            if (len(tds)>0):
                #print("+++",tds[0].contents[0])
                rows=[]
                for idx,td in enumerate(tds):
                    #lines.append(td.getText())
                    str=td.getText().replace('\t','').replace('\n','').strip()
                    #print(str)
                    rows.append(str)
                    #print(idx,"=",td.getText())

                #print(rows)
                #print(td.find(text=True))
            if ('日期' in rows[0]):
                find=True
                continue
            if find:
                data_list.append(rows)
        if find:
            return code, name, data_list
    return code, name, data_list

def parse_sina_data(filepathname,to_filepathname):
    if os.path.isfile(filepathname):
        filename = os.path.basename(filepathname)
        farray=filename.split('-')
        code=farray[1].strip()
        (code,name,data_list)=parser_html_from_sina(filepathname)
        print(code,name,data_list)
        #ret=input2db(code,name,data_list,filename)
        f = open(to_filepathname, 'w')
        if len(data_list) <= 0:
            f.write(" ")
        else:
            idx = 0
            for line in data_list:
                idx += 1
                print(line)
                date = line[0]
                begin = line[1]
                high = line[2]
                price = line[3]
                low = line[4]
                volume = line[5]
                money = line[6]
                # ----
                data_from = 'sina'  #
                create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(date, ',', code, ':', name)
                insert_sql = 'insert into inputsina (date,code,name,begin,low,high,price,volume,money,data_from,create_time)'
                insert_sql += 'values ("%s","%s","%s","%s","%s","%s" , "%s" , "%s", "%s", "%s", "%s")'
                insert_sql = insert_sql % (
                date, code, name, begin, low, high, price, volume, money, data_from, create_time)
                f.write(insert_sql+'\n')
                # log("%d,%s" % (idx, insert_sql))
        f.close()
    pass

if __name__ == "__main__":

    allArgvs = sys.argv[1:]
    if not(len(allArgvs) ==0 or len(allArgvs) ==2):
        readme()
        exit(1)

    if len(allArgvs) ==2:
        from_sinadir = sys.argv[1]
        to_sinadir = sys.argv[2]
    else:
        root_dir = os.getcwd()
        download_file_dir = os.path.join(root_dir, "download")
        from_sinadir = os.path.join(download_file_dir, "sina")
        to_sinadir = os.path.join(download_file_dir, "sina_data")

    print(from_sinadir)
    print(to_sinadir)
    if not os.path.exists(from_sinadir):
        log("Error: sourceDir not found: %s"%from_sinadir)
        exit(0)
    if not os.path.exists(from_sinadir):
        log("Error: destDir not found: %s" % to_sinadir)
        exit(0)
    #--
    if os.path.isfile(from_sinadir): #support sina_html_file to sina_data_file
        parse_sina_data(from_sinadir, to_sinadir);
        exit()
    #---
    list=os.listdir(from_sinadir)
    list.sort()
    n=0
    if (len(list)>0):
        for file in list:
            n += 1
            filename = os.path.basename(file)
            print(n,':',filename)
            filepathname = os.path.join(from_sinadir, filename)
            to_filepathname = os.path.join(to_sinadir, filename)
            if os.path.isfile(filepathname):
                parse_sina_data(filepathname,to_filepathname);
            #break #### for test , one file
    pass