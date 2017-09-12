#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import time,datetime
import glob


from xml.dom.minidom import parse
import xml.dom.minidom


import urllib
import os

from urllib import request
import shutil
from bs4 import BeautifulSoup

atime = datetime.datetime.now().strftime("%Y-%m-%d")  # '2017-07-20'
adate = time.strptime(atime, '%Y-%m-%d')
date1 = datetime.date(adate.tm_year, adate.tm_mon, adate.tm_mday)
for count in range(10):
    print(count)
    add_date = datetime.timedelta(days=count)
    date2 = date1 - add_date
    strDate=date2.strftime("%Y-%m-%d")
    # url = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1815_stock&txtBeginDate=2017-07-21&txtEndDate=2017-07-21&tab1PAGENO=1&ENCODE=1&TABKEY=tab1 HTTP/1.1'
    # file="c:/rd/1.xls"
    url1 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1815_stock&txtBeginDate='
    url2 = '&txtEndDate='
    url3 = '&tab1PAGENO=1&ENCODE=1&TABKEY=tab1'
    url = ("%s%s%s%s%s" % (url1, strDate, url2, strDate, url3))
    print(url)


