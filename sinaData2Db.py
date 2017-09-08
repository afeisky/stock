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
import codecs
import shutil
from bs4 import BeautifulSoup

__DONNOT_DOWNLOAD_EXIST_FILE=1

global LogOut

##pip3 install xlrd


def log(string):
    #global LogOut
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    if ('Error:' in string) or ('ERROR:' in string):
         print("\033[31;1m%s\033[0m"%string)
    else:
        print("%s\n"%string)
    #LogOut.write("%s\n"%string)

class Database():
    conn = mysql.connector.connect(user='root', password='chaofei1',host='127.0.0.1',port='3306',database='afei')
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

def save2db(insert_sql):
    #Database().execSQL(insert_sql)
    print(insert_sql)
    conn = mysql.connector.connect(user='root', password='chaofei1', host='127.0.0.1', port='3306', database='afei')
    cursor = conn.cursor()
    cursor.execute(insert_sql)
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    root_dir = os.getcwd()
    dir1 = os.path.join(root_dir, "download")
    dirData = os.path.join(dir1, "sina_data")

    list=os.listdir(dirData)
    list.sort()
    n=0
    if (len(list)>0):
        conn = mysql.connector.connect(user='root', password='chaofei1', host='127.0.0.1', port='3306',
                                       database='afei')
        for file in list:
            n += 1
            filename = os.path.basename(file)
            filepathname = os.path.join(dirData, filename)
            if (os.path.getsize(filepathname)) < 10:
                log("%5d:%s %s"%(n,filename," -- Fail! Error:"))
                continue
            log("%5d:%s"%(n,filename))
            with open(filepathname, 'r') as f:
                while True:
                    line=f.readline()
                    if not line:
                        break
                    else:
                        cursor = conn.cursor()
                        cursor.execute(line)
                        conn.commit()
                        cursor.close()
                        pass
                f.close()
        conn.close()
        pass
    #LogOut.close()

