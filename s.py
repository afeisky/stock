#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import time,datetime
import glob
from time import *
import urllib
import os

from urllib import request
import shutil
import sse
import szse
import sinaDownload
if __name__ == '__main__':


    sinaDownload.main([])

    exit(1)
    sse_download_dir='../download/sse'
    param=['download',sse_download_dir]
    sse.main(param)
    #---
    szse_download_dir = '../download/szse'
    param=['download','2017-06-07','2017-09-07',szse_download_dir]
    sse.szse(param)

    param=['input2db',sse_download_dir]
    sse.main(param)
    param=['input2db',szse_download_dir]
    szse.szse(param)


#