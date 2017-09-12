#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from urllib import request
import os,sys
import datetime
import time
import mysql
from mysql import connector
import xlrd


#mysqldump -uchaofei -h127.0.0.1 -P3307  chaofei input> f:\my_tools\mysql\backup_chaofei.sql


# File->Settings->Project:untitled->Project Interpreter: + -> search "XlsxWriter" -> 选中版本号0.9.8  -> install packages.
# or 下面这个办法
# C:\Python34\Scripts>pip install ../xlrd-1.0.0   #先从https://pypi.python.org/pypi网站上下载xlrd-1.0.0.tar.gz文件，解压缩。
#    C:\Python34\Scripts>pip install ../xlrd-1.0.0
#    Processing c:\python34\xlrd-1.0.0
#    Installing collected packages: xlrd
#      Running setup.py install for xlrd
#    Successfully installed xlrd-1.0.0

# pip install -U ../beautifulsoup4-4.6.0
#  https://www.crummy.com/software/BeautifulSoup/

__DONNOT_DOWNLOAD_EXIST_FILE=0


#global LogOut

def log(string):
    #global LogOut
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    if ('Error:' in string) or ('ERROR:' in string):
         print("\033[31;1m %s\033[0m"%string)
    else:
        print("%s\n"%string)
    #LogOut.write("%s\n"%string)

def readme():
    print("usage: python3 szse.py download begin_date  end_date download_dir")
    print("       python3 szse.py download 2017-08-01  2017-08-31 ./download_szse")
    print("       python3 szse.py input2db ./download_szse")


def download_url(url,filePathName,downloadExists=False):
    print(url)
    print(filePathName)
    (filepath,tempfilename) = os.path.split(filePathName);
    (shotname,extension) = os.path.splitext(tempfilename);
    if os.path.exists(filePathName) and (os.path.getsize(filePathName)) < 3000:  # .获取文件大小, 使用os.path.getsize函数，参数是文件的路径。
        log('Error: delete %s' % filePathName)
        os.remove(filePathName)
    if (not downloadExists) and os.path.exists(filePathName):
        log("Warnning: %s file exist, donnot download!"%filePathName)
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
            log("====> %s file not exist, need download!"%filePathName)
        return filePathName
    except:
        log('[readExcel] Error: filePathName=%s no data!'%(shotname))
        return ""

def download_sz_a(strDate, filePathName):
    # url = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1815_stock&txtBeginDate=2017-07-21&txtEndDate=2017-07-21&tab1PAGENO=1&ENCODE=1&TABKEY=tab1 HTTP/1.1'
    # file="c:/rd/1.xls"
    url1 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1815_stock&txtBeginDate='
    url2 = '&txtEndDate='
    url3 = '&tab1PAGENO=1&ENCODE=1&TABKEY=tab1'
    url = ("%s%s%s%s%s" % (url1, strDate, url2, strDate, url3))
    #print(url)
    #print(filePathName)
    return url, filePathName


def download_sz(begin_date, end_date, download_dir):
    d = begin_date
    add_date = datetime.timedelta(days=1)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(download_dir):
        print("Error: %s is not found!" % download_dir)
    while d <= end_date:
        ret = download_sz_a(d.strftime("%Y-%m-%d"), os.path.join(download_dir, d.strftime("szse_%Y-%m-%d.xlsx")))
        d += add_date

def szse_readExcel(filename):
    lists=[]
    print(filename)
    if not os.path.exists(filename):
        print("Error: %s is not found!"%filename)
        return lists
    workbook=xlrd.open_workbook(filename)

    #sheet
    all_sheets_list=workbook.sheet_names()
    #print("All sheets name in File:",all_sheets_list)

    first_sheet=workbook.sheet_by_index(0)
    #print("First sheet Name:",first_sheet.name)
    print("First sheet Rows:",first_sheet.nrows)
    #print("First sheet Cols:",first_sheet.ncols)

    #first_row=first_sheet.row_values(0)
    #print("First row:",first_row)
    #first_col=first_sheet.col_values(0)
    #print("First Column:",first_col)

    if (first_sheet.nrows<10):
        return lists

    #print("row0:%s"%first_sheet.row_values(0))
    #print("row0:%s"%first_sheet.row_values(1))
    #print("row0:%s"%first_sheet.row_values(2))

    colDateList=[]
    for index,value in enumerate(first_sheet.row_values(0)):
        if ('日期' in value) or ('时间' in value):
            colDateList.append(index)
    print(colDateList)

    try:
        log("%s: rows/cols (%d,%d)"%(filename,first_sheet.nrows,first_sheet.ncols))
        for row in range(1,(first_sheet.nrows)):
            input_date=''
            input_code=''
            input_name=''
            input_last=''
            input_now=0
            input_percent=0
            input_memoy=0
            input_peraito=0

            for col in range(0,(first_sheet.ncols)):
                value=first_sheet.cell(row,col).value
                celltype=first_sheet.cell_type(row,col)
                if (col==0): # col in colDateList:
                    print("0: celltype=%d"%celltype)
                    if celltype==3: # is float?
                        value=xlrd.xldate_as_tuple(value,0) #转化为元组形式
                        value="%d-%02d-%02d"%(value[0],value[1],value[2])
                        #value=xlrd.xldate.xldate_as_datetime(value,1) #直接转化为datetime对象
                    print("%s,%s:%s"%(row,col,value))
                elif (col==1):
                    print("1: celltype=%d"%celltype)
                    if celltype==2: # is float
                        valueStr=str(value)
                        value=valueStr[:len(valueStr)-2]
                    print("%s,%s:%s"%(row,col,value))
                elif (col==6):#momey
                    value=value.replace(',','')
                elif (col==7):#momey
                    value=value.replace(',','')
                else:
                    print("%s,%s:%s"%(row,col,value))
                if col==0:
                    input_date=value
                elif col==1:
                    input_code=value
                elif col==2:
                    input_name=value
                elif col==3:
                    input_last=value
                elif col==4:
                    input_now=value
                elif col==5:
                    input_percent=value
                elif col==6:
                    input_memoy=value
                elif col==7:
                    if value=="" :
                        input_peraito=0
                    else:
                        input_peraito=value
                else:
                    pass
            create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_sql = 'insert into chaofei.input (date,code,name,last,now,percent,money,peratio,data_from,create_time)values '
            sql_values='("%s" , "%s" ,"%s" , "%s" , "%s" , "%s" , "%s" , "%s", "%s")'
            insert_sql=sql_values%(input_date,input_code,input_name,input_last,input_now,input_percent,input_memoy,input_peraito,"www.szse.cn")
            log(insert_sql)
            lists.append(insert_sql)
        return lists
    except:
        log("[readExcel] Error: %s no data!"%(filename))
        return []
    finally:
        log("[readExcel] %s done."%(filename))
        return lists



'''
def input_from_web():
    cnx = mysql.connector.connect(user='chaofei', password='chaofei1',host='127.0.0.1',port='3307',database='chaofei')

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM table1;')

    #("SELECT * FROM CITY where CountryCode = %(country)s", {'country':country})
    #cursor.execute('insert table1 (ids,code) values(1,"00100021");')
    #cnx.commit()
    cities = cursor.fetchall()
    print(cities)
    cnx.close()

    cnx = mysql.connector.connect(user='qdb1', password='qdb1', host='170.19.17.9', database='qdb1')
    cursor = cnx.cursor()

    insert_sql = ("insert into qdb1.amis"
                  " (CUSTOMER_NAME, AWS_ACCOUNT, AMI_START, CRT_REGION_PRIMARY, CRT_REGION_DR1, CRT_REGION_DR2, DBAPP_INST_ID, DBAPP_AMI_ID, DBAPP_AMI_NAME, VISTA_INST_ID, VISTA_AMI_ID, VISTA_AMI_NAME, WS_INST_ID, WS_AMI_ID, WS_AMI_NAME, DEL_REGION_PRIMARY, DEL_REGION_DR1, DEL_REGION_DR2, DELETED_AMI_PRIMARY, DELETED_SNAP_PRIMARY, DELETED_AMI_DR1, DELETED_SNAP_DR1, DELETED_AMI_DR2, DELETED_SNAP_DR2, SUCCESSFUL) "
                  "values ( %(CUSTOMER_NAME)s , %(AWS_ACCOUNT)s , %(AMI_START)s , %(CRT_REGION_PRIMARY)s , %(CRT_REGION_DR1)s , %(CRT_REGION_DR2)s , %(DBAPP_INST_ID)s , %(DBAPP_AMI_ID)s , %(DBAPP_AMI_NAME)s , %(VISTA_INST_ID)s , %(VISTA_AMI_ID)s , %(VISTA_AMI_NAME)s , %(WS_INST_ID)s , %(WS_AMI_ID)s , %(WS_AMI_NAME)s , %(DEL_REGION_PRIMARY)s , %(DEL_REGION_DR1)s , %(DEL_REGION_DR2)s , %(DELETED_AMI_PRIMARY)s , %(DELETED_SNAP_PRIMARY)s , %(DELETED_AMI_DR1)s , %(DELETED_SNAP_DR1)s , %(DELETED_AMI_DR2)s , %(DELETED_SNAP_DR2)s , %(SUCCESSFUL)s)")

    print(insert_sql)

    insert_data = ('SERVER1', '68687687876','2014-12-29 13:27:46', 'us-west-9', 'None', 'None', 'i-gtsuid43', 'ami-9jsh222f', 'DBAPP-SERVER', 'i-4wj333e3', 'ami-73eee351', 'VISTA-SERVER', 'i-5464ssse', 'ami-4ddd2853', 'WS-QSERVER', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 1)

    cursor.executemany(insert_sql, insert_data)
    cnx.commit()
    cursor.close()
'''


if __name__ == "__main__":
    #################
    #mysql: 127.0.0.1:3307  user&password: root:tcl123+,  adminuser: chaofei:chaofei1
    ####################
    #LogOut= open(os.path.join(os.getcwd(),"out.log"),'w')
    if len(sys.argv[1:])<2:
        readme()
        exit()
    allArgvs = sys.argv[1:]

    if sys.argv[1]=='download':
        begin_date=sys.argv[2]
        end_date = sys.argv[3]
        download_dir = sys.argv[4]
        #print(begin_date, '->', end_date)
        begin_date1 = time.strptime(begin_date,"%Y-%m-%d")
        end_date1 = time.strptime(end_date, "%Y-%m-%d")
        #begin = datetime.date(2017,7,30)
        #end = datetime.date(2017,7,31)
        begin = datetime.date(begin_date1.tm_year,begin_date1.tm_mon,begin_date1.tm_mday)
        end = datetime.date(end_date1.tm_year,end_date1.tm_mon,end_date1.tm_mday)
        print('download:', begin, '->', end, 'to [' + download_dir + ']')
        if download_dir[:1] == '/' or download_dir[1:2] == ':':
            root_dir = os.getcwd()
            download_dir = os.path.join(root_dir, download_dir)
        if not os.path.exists(download_dir):
            log('Error: not found dir: %s' % download_dir)
            exit(0)
        download_sz(begin,end,download_dir)
    elif sys.argv[1] == 'input2db':
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
            fdata= open(os.path.join(os.getcwd(),"szse_out.log"),'w')
            conn = mysql.connector.connect(user='root', password='chaofei1',
                                           host='127.0.0.1', port='3306', database='afei')
            insert_sql = 'insert into in_szse_tmp (date,code,name,last,price,percent,money,peratio,data_from) values '
            for file in listdir:
                filename = os.path.basename(file)
                #print(filename)
                #print(filename[:5])
                #print(filename[-5:len(filename)])
                if not (filename[:5] == 'szse_' and filename[-5:len(filename)] == '.xlsx'):
                    break
                filepathname = os.path.join(download_dir, filename)
                #if (os.path.getsize(filepathname)) < 10:
                #    log("%5d:%s %s" % (n, filename, " -- Fail! Error:"))
                #    continue
                listdata = szse_readExcel(filepathname)
                #if len(listdata)==0:
                #    fdata.write("Error! "+filename+'\n')
                for line in listdata:
                    cursor = conn.cursor()
                    line=insert_sql + ' ' + line
                    cursor.execute(line)
                    conn.commit()
                    cursor.close()
                    fdata.write(line+'\n')
            conn.close()
            fdata.close()

    else:
        readme()
        exit(1)

########################################################################