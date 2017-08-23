# -*- coding: UTF-8 -*-
import sys
import urllib2
import json
import MySQLdb
import options
import os
import requests
import execjs
from os.path import dirname,join,abspath
from options import *
from logger import *
import time

reload(sys)  
sys.setdefaultencoding('utf8')
class Spider(object):
	def __init__(self):
		print "load workpy"

	def main(self,obj):
		total_count = self.spiderOption(obj)
		return total_count

	def spiderOption(self,obj):
		count = obj.budejieSpider(1,self)
		count += obj.budejieSpider(2,self)
		count += obj.baiduSpider(1,self)
		count += obj.baiduSpider(2,self)
		count += obj.inkeSpider(self)
		count += obj.momoSpider(self)
		count += obj.huoshanSpider(self)
		count += obj.kuaishouSpider(self)
		count += obj.kuaishipinSpider(self)
		count += obj.toutiaoSpider(self)
		return count

	def	connMysql(self):
		conn= MySQLdb.connect(
		        host='127.0.0.1',
		        port = 3306,
		        user='root',
		        passwd='',
		        db ='test',
		    )
		return conn	
		
	def checkRepeat(self,cur,source,source_id):
		result = cur.execute("SELECT id from spider_video WHERE source=%s AND source_id=%s",(source,source_id))
		return result

	def closeMysql(self,conn):
		conn.commit()
		conn.close()

if __name__ == '__main__':
	spider = Spider()
	logger = Logger()
	info_logger = logger.infoLogger()
	debug_logger = logger.debugLogger()
	warn_logger = logger.warnLogger()
	opt = Options(info_logger,debug_logger,warn_logger)
	total_count = 0
	while True:
		count = spider.main(opt)
		total_count += count
		info_logger.info('Save Total Count: %s ' % (total_count))
		time.sleep(180)