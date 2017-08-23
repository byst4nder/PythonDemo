# -*- coding: UTF-8 -*-
import sys
import urllib2
import urllib
import json
import MySQLdb
import execjs
import re
import requests
import random
import time
import base64

reload(sys)  
sys.setdefaultencoding('utf8')
class Options(object):
	def __init__(self,info_logger,debug_logger,warn_logger):
		self.info_logger = info_logger
		self.debug_logger = debug_logger
		self.warn_logger = warn_logger

	def budejieSpider(self,urlType,obj):
		from_url1 = 'http://d.api.budejie.com/topic/list/chuanyue/41/budejie-android-6.7.0/0-99.json?market=yingyongbao&ver=6.7.0&visiting=&os=6.0&appname=baisibudejie&client=android&udid=862823033197288&mac=02:00:00:00:00:00'
		from_url2 = 'http://s.budejie.com/topic/list/jingxuan/41/budejie-android-6.7.0/0-99.json?market=yingyongbao&ver=6.7.0&visiting=&os=6.0&appname=baisibudejie&client=android&udid=862823033197288&mac=02:00:00:00:00:00'
		if urlType == 1 :
			response = urllib2.urlopen(from_url1) 
		else:
			response = 	urllib2.urlopen(from_url2)  
		response_text = response.read()
		dataArr = json.loads(response_text, encoding='utf-8')
		dataList = dataArr['list']
		total_count = dataArr['info']['count']
		conn = obj.connMysql()
		cur = conn.cursor()
		t_count = 1
		try:
			cur.execute('SET NAMES utf8;')
			cur.execute('SET CHARACTER SET utf8;')
			cur.execute('SET character_set_connection=utf8;')
			sql = "insert into spider_video (title,url,source_id,source,description,status,thumbnail_cover,width,height) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			for index,value in enumerate(dataList):
				title = base64.b64encode(dataList[index]['text'])
				url = dataList[index]['video']['video'][0]
				source_id = dataList[index]['id']
				source = 'bsbdj'
				data = obj.checkRepeat( cur, source, source_id)
				if data > 0:
					self.debug_logger.debug('%s : %s  exist' % (source, source_id))
					continue
				description = base64.b64encode(dataList[index]['text'])
				status = 0
				thumbnail_cover = dataList[index]['video']['thumbnail'][0]
				width = dataList[index]['video']['width']
				height = dataList[index]['video']['height']
				cur.execute(sql,(title,url,source_id,source,description,status,thumbnail_cover,width,height))
				self.debug_logger.debug('%s : %s insert success' % (source, source_id))
				t_count += 1
			cur.close()
			obj.closeMysql(conn)
			return t_count
		except MySQLdb.Error, e:
			try:
				self.warn_logger.warn("Error %d:%s" % (e.args[0], e.args[1]))
				return 0
			except IndexError:
				self.warn_logger.warn("MySQL Error:%s" % str(e))
				return 0

	def inkeSpider(self,obj):
		url = 'http://116.211.167.106/api/feeds_tab/recommends?cc=TG36001&lc=317d503b3fb586f4&mtxid=882593b8e0e8&devi=866656020839181&sid=20zlC2uIVIzKNkWi0TG9GCazXw5ySHpeIi0e5o5K2T1ti2ualvpoj&osversion=android_23&cv=IK4.0.10_Android&imei=866656020839181&proto=7&conn=WIFI&ua=HUAWEIALE-TL00&logid=162,127,45,210&uid=417976965&icc=&vv=1.0.3-201610121413.android&aid=16e1e3129d71a70b&smid=DueJxrQ+n/dXzyotxnI3LbnpQ3zde19gDFNd8MCLdXE7F4DF0pI3MoKW2YVAP3UX9pewLNXJ1NA8UblAbxp3qaMg&imsi=&mtid=cdd986e7f47c68e598c2367637a16237&start=800&limit=30&r_c=39868841&s_sg=d1eb7c8ad628a598e6f3de914a38d84a&s_sc=100&s_st=1494470020';
		response = urllib2.urlopen(url) 
		response_text = response.read()
		dataArr = json.loads(response_text, encoding='utf-8')
		if dataArr['dm_error'] > 0:
			return
		dataList = dataArr['feeds']	
		total_count = dataArr['total']
		conn = obj.connMysql()
		cur = conn.cursor()
		t_count = 1
		try:
			cur.execute('SET NAMES utf8;')
			cur.execute('SET CHARACTER SET utf8;')
			cur.execute('SET character_set_connection=utf8;')
			sql = "insert into spider_video (title,url,source_id,source,description,status,thumbnail_cover,width,height,duration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			for index,value in enumerate(dataList):
				videoInfo = json.loads(dataList[index]['content'], encoding='utf-8')
				if dataList[index]['title'] == "":
					dataList[index]['title'] = " "
				title = base64.b64encode(dataList[index]['title'])
				url = videoInfo['mp4_url']
				source_id = dataList[index]['feedId']
				source = 'inke'
				data = obj.checkRepeat( cur, source, source_id)
				if data > 0:
					self.debug_logger.debug('%s : %s  exist' % (source, source_id))
					continue
				description = base64.b64encode(dataList[index]['title'])
				status = 0
				thumbnail_cover = videoInfo['cover_url']
				duration = dataList[index]['duration']
				width = 0
				height = 0
				cur.execute(sql,(title,url,source_id,source,description,status,thumbnail_cover,width,height,duration))
				self.debug_logger.debug('%s : %s insert success' % (source, source_id))
				t_count += 1
			cur.close()
			obj.closeMysql(conn)
			return t_count
		except MySQLdb.Error, e:
			try:
				self.warn_logger.warn("Error %d:%s" % (e.args[0], e.args[1]))
				return 0
			except IndexError:
				self.warn_logger.warn("MySQL Error:%s" % str(e))
				return 0

	def baiduSpider(self,urlType,obj):
		from_url1 = 'https://sv.baidu.com/platapi/v2/video_list?from=rec&rn=99&lid=947a4711ba3aaeb66dd552a2486fb543&cuid=&tag=doubiju&bid=E04B53E1804263C5153C99A4C9CD374A:FG=1&cb_cursor=undefined&hot_cursor=undefined&offline_cursor=undefined&cursor_time=undefined&sessionid=E04B53E1804263C5153C99A4C9CD374A:FG=1&vsid=80000002&swd=414&sht=736'
		from_url2 = 'https://sv.baidu.com/platapi/v2/video_list?from=rec&rn=100&lid=e9550107bdaedafaaf08f5f346453df5&cuid=&tag=recommend&bid=E04B53E1804263C5153C99A4C9CD374A:FG=1&cb_cursor=0&hot_cursor=0&offline_cursor=0&cursor_time=0&sessionid=E04B53E1804263C5153C99A4C9CD374A:FG=1&vsid=80000002'
		if urlType == 1 :
			response = urllib2.urlopen(from_url1)
		else:
			response = 	urllib2.urlopen(from_url2)
		response_text = response.read()
		dataArr = json.loads(response_text, encoding='utf-8')
		if dataArr['errno'] > 0:
			return 0
		dataList = dataArr['data']['list']
		total_count = len(dataArr)
		conn = obj.connMysql()
		cur = conn.cursor()
		t_count = 1
		try:
			cur.execute('SET NAMES utf8;')
			cur.execute('SET CHARACTER SET utf8;')
			cur.execute('SET character_set_connection=utf8;')
			sql = "insert into spider_video (title,url,source_id,source,description,status,thumbnail_cover,width,height,duration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			for index,value in enumerate(dataList):
				title = base64.b64encode(dataList[index]['title'])
				url = dataList[index]['video_src']
				source_id = dataList[index]['vid']
				source = 'baidu'
				data = obj.checkRepeat( cur, source, source_id)
				if data > 0:
					self.debug_logger.debug('%s : %s  exist' % (source, source_id))
					continue
				description = base64.b64encode(dataList[index]['title'])
				status = 0
				thumbnail_cover = dataList[index]['thumbnails']
				duration = dataList[index]['duration']
				width = 0
				height = 0
				cur.execute(sql,(title,url,source_id,source,description,status,thumbnail_cover,width,height,duration))
				self.debug_logger.debug('%s : %s insert success' % (source, source_id))
				t_count += 1
			cur.close()
			obj.closeMysql(conn)
			return t_count
		except MySQLdb.Error, e:
			try:
				self.warn_logger.warn("Error %d:%s" % (e.args[0], e.args[1]))
				return 0
			except IndexError:
				self.warn_logger.warn("MySQL Error:%s" % str(e))
				return 0

	def momoSpider(self	,obj):
		url = 'http://m.immomo.com/inc/microvideo/share/recommends?page_rows=400';
		response = urllib2.urlopen(url)
		response_text = response.read()
		dataArr = json.loads(response_text, encoding='utf-8')
		if (dataArr['ec'] != 200) :
			return
		if (dataArr['em'] != 'ok') :
			return
		dataList = dataArr['data']['list']
		conn = obj.connMysql()
		cur = conn.cursor()
		t_count = 1
		try:
			cur.execute('SET NAMES utf8;')
			cur.execute('SET CHARACTER SET utf8;')
			cur.execute('SET character_set_connection=utf8;')
			sql = "insert into spider_video (title,url,source_id,source,description,status,thumbnail_cover,width,height,duration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			for index, value in enumerate(dataList):
				dataList[index]['title'] = ""
				title = base64.b64encode(dataList[index]['title'])
				url = dataList[index]['video_url']
				source_id = dataList[index]['feedid']
				source = 'momo'
				data = obj.checkRepeat(cur, source, source_id)
				if data > 0:
					self.debug_logger.debug('%s : %s  exist' % (source, source_id))
					continue
				description = base64.b64encode(dataList[index]['title'])
				status = 0
				thumbnail_cover = dataList[index]['cover']['l']
				duration = 0
				width = 0
				height = 0
				cur.execute(sql, (title, url, source_id, source, description, status, thumbnail_cover, width, height, duration))
				self.debug_logger.debug('%s : %s insert success' % (source, source_id))
				t_count += 1
			cur.close()
			obj.closeMysql(conn)
			return t_count
		except MySQLdb.Error, e:
			try:
				self.warn_logger.warn("Error %d:%s" % (e.args[0], e.args[1]))
				return 0
			except IndexError:
				self.warn_logger.warn("MySQL Error:%s" % str(e))
				return 0

	def huoshanSpider(self, obj):
		url = 'https://www.huoshan.com/share/hot_videos/?offset=0&count=400'
		response = urllib2.urlopen(url)
		response_text = response.read()
		dataArr = json.loads(response_text, encoding='utf-8')
		if (dataArr['status_code'] > 0):
			return 0
		dataList = dataArr['data']
		conn = obj.connMysql()
		cur = conn.cursor()
		t_count = 1
		try:
			cur.execute('SET NAMES utf8;')
			cur.execute('SET CHARACTER SET utf8;')
			cur.execute('SET character_set_connection=utf8;')
			sql = "insert into spider_video (title,url,source_id,source,description,status,thumbnail_cover,width,height,duration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			for index, value in enumerate(dataList):
				title = base64.b64encode(dataList[index]['text'])
				videoList = dataList[index]['video']
				target_url = videoList['url_list'][0]
				target_url = target_url.replace('watermark=1', 'watermark=0')
				req = urllib2.urlopen(target_url)
				url = req.geturl()
				source_id = dataList[index]['id']
				source = 'huoshan'
				data = obj.checkRepeat(cur, source, source_id)
				if data > 0:
					continue
				description = base64.b64encode(dataList[index]['text'])
				status = 0
				thumbnail_cover = videoList['cover']['url_list'][0]
				duration = videoList['duration']
				width = videoList['width']
				height = videoList['height']
				cur.execute(sql, (
				title, url, source_id, source, description, status, thumbnail_cover, width, height, duration))
				self.debug_logger.debug('%s : %s insert success' % (source, source_id))
				t_count += 1
			cur.close()
			obj.closeMysql(conn)
			return t_count
		except MySQLdb.Error, e:
			try:
				self.warn_logger.warn("Error %d:%s" % (e.args[0], e.args[1]))
				return 0
			except IndexError:
				self.warn_logger.warn("MySQL Error:%s" % str(e))
				return 0

	def kuaishouSpider(self,obj):
		url = 'http://101.251.217.210/rest/n/feed/list?mod=Xiaomi(Redmi%204)&lon=114.053918&country_code=CN&did=ANDROID_46056840cbdcccfe&app=0&net=WIFI&oc=UNKNOWN&ud=528634063&c=XIAOMI&sys=ANDROID_6.0.1&appver=4.56.0.4297&language=zh-cn&lat=22.537537&ver=4.56'
		params = {'type':7,'page':2,'count':20,'pv':'false','id':46,'pcursor':'','__NStokensig':'78342d9929ce7f7a3e6c8a8fd6f2ed3fb68577cd8f235cba9fcfb58cce47260a','token':'e949a8c2df4b4c1fb29a783ac9762e2b-528634063','client_key':'3c2cd3f3','os':'android','sig':'79f065d2e57271e1af61b5e5afeaa1ed'}
		params = urllib.urlencode(params)
		response = urllib2.urlopen(url,params)
		response_text = ''.join(response)
		dataArr = json.loads(response_text, encoding='utf-8')
		print dataArr['result']
		if (dataArr['result'] != 1):
			return 0
		dataList = dataArr['feeds']
		conn = obj.connMysql()
		cur = conn.cursor()
		t_count = 0
		try:
			cur.execute('SET NAMES utf8;')
			cur.execute('SET CHARACTER SET utf8;')
			cur.execute('SET character_set_connection=utf8;')
			sql = "insert into spider_video (title,url,source_id,source,description,status,thumbnail_cover,width,height,duration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			for index,value in enumerate(dataList):
				dataList[index]['caption'] = dataList[index]['caption'].replace(u"快手", "")
				title = base64.b64encode(dataList[index]['caption'])
				description = base64.b64encode(dataList[index]['caption'])
				thumbnail_cover = dataList[index]['cover_thumbnail_urls'][0]['url']
				source = 'kuaishou'
				source_id = dataList[index]['timestamp']
				data = obj.checkRepeat(cur, source, source_id)
				if data > 0:
					print '%s : %s exist' % (source, source_id)
					continue
				width = dataList[index]['ext_params']['w']
				height = dataList[index]['ext_params']['h']
				url = dataList[index]['main_mv_urls'][0]['url']
				status = 0
				duration = 0
				cur.execute(sql, (title, url, source_id, source, description, status, thumbnail_cover, width, height, duration))
				self.debug_logger.debug('%s : %s insert success' % (source, source_id))
				t_count += 1
			cur.close()
			obj.closeMysql(conn)
			return t_count
		except MySQLdb.Error, e:
			try:
				self.warn_logger.warn("Error %d:%s" % (e.args[0], e.args[1]))
				return 0
			except IndexError:
				self.warn_logger.warn("MySQL Error:%s" % str(e))
				return 0

	def kuaishipinSpider(self,obj):
		url = 'http://v.sj.360.cn/pc/list?n=10&p=1&f=json&ajax=1&uid=d5857958332acd8470ccfeafa337556d&channel_id=0'
		response = urllib2.urlopen(url)
		response_text = response.read()
		dataArr = json.loads(response_text, encoding='utf-8')
		if (dataArr['errno'] > 0):
			return 0
		dataList = dataArr['data']['res']
		conn = obj.connMysql()
		cur = conn.cursor()
		t_count = 0
		try:
			cur.execute('SET NAMES utf8;')
			cur.execute('SET CHARACTER SET utf8;')
			cur.execute('SET character_set_connection=utf8;')
			sql = "insert into spider_video (title,url,source_id,source,description,status,thumbnail_cover,width,height,duration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			for index, value in enumerate(dataList):
				if (dataList[index]['c'] != 'video') :
					continue
				title = base64.b64encode(dataList[index]['t'])
				videoData = dataList[index]['exData']
				target_url = videoData['playLink']
				try:
					response = urllib2.urlopen(target_url)
					response_text = response.read()
					dataArr = json.loads(response_text, encoding='utf-8')
					if (dataArr['errno'] > 0):
						continue
					url = dataArr['data']['url']
					source_id = videoData['code']
					source = '360'
					data = obj.checkRepeat(cur, source, source_id)
					if data > 0:
						print '%s : %s exist' % (source, source_id)
						continue
					description = base64.b64encode(dataList[index]['t'])
					status = 0
					thumbnail_cover = videoData['picUrl']
					duration = 0
					width = 0
					height = 0
					cur.execute(sql, (title, url, source_id, source, description, status, thumbnail_cover, width, height, duration))
					self.debug_logger.debug('%s : %s insert success' % (source, source_id))
					t_count += 1
				except urllib2.URLError, e:
					self.info_logger.info("urlopen fail reason: %s" % (e.reason))
					continue
			cur.close()
			obj.closeMysql(conn)
			return t_count
		except MySQLdb.Error, e:
			try:
				self.warn_logger.warn("Error %d:%s" % (e.args[0], e.args[1]))
				return 0
			except IndexError:
				self.warn_logger.warn("MySQL Error:%s" % str(e))
				return 0

	def toutiaoSpider(self,obj):
		times = int(time.time())
		url = 'https://www.toutiao.com/api/pc/feed/?category=video&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=%s&tadrequire=true' % times
		response = urllib2.urlopen(url)
		response_text = response.read()
		dataArr = json.loads(response_text, encoding='utf-8')
		if (dataArr['message'] != 'success'):
			return 0
		dataList = dataArr['data']
		conn = obj.connMysql()
		cur = conn.cursor()
		t_count = 0
		try:
			cur.execute('SET NAMES utf8;')
			cur.execute('SET CHARACTER SET utf8;')
			cur.execute('SET character_set_connection=utf8;')
			sql = "insert into spider_video (title,url,source_id,source,description,status,thumbnail_cover,width,height,duration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			for index, value in enumerate(dataList):
				if dataList[index]['has_video'] is False :
					continue
				title = base64.b64encode(dataList[index]['title'])
				if dataList[index].has_key('video_id') is False :
					continue
				video_id = dataList[index]['video_id']
				source_id = video_id
				source = 'toutiao'
				data = obj.checkRepeat(cur, source, source_id)
				if data > 0:
					continue
				description = base64.b64encode(dataList[index]['title'])
				ctx = open('jrtt.js', 'r')
				js = ctx.read()
				runjs = execjs.compile(js)
				vurl = runjs.call("new_crc32", video_id)
				try:
					req = urllib2.urlopen(vurl, timeout=20)
					req_text = req.read()
					childData = json.loads(req_text, encoding='utf-8')
					if (childData['code'] != 0):
						continue
					duration = childData['data']['video_duration']
					thumbnail_cover = ''
					if childData['data'].has_key('big_thumbs'):
						thumbnail_cover = childData['data']['big_thumbs'][0]['img_url']
					if (len(childData['data']['video_list']) < 3):
						url = base64.b64decode(childData['data']['video_list']['video_1']['main_url'])
						width = childData['data']['video_list']['video_1']['vwidth']
						height = childData['data']['video_list']['video_1']['vheight']
					else:
						url = base64.b64decode(childData['data']['video_list']['video_3']['main_url'])
						width = childData['data']['video_list']['video_3']['vwidth']
						height = childData['data']['video_list']['video_3']['vheight']
					status = 0
					cur.execute(sql, (
						title, url, source_id, source, description, status, thumbnail_cover, width, height, duration))
					self.debug_logger.debug('%s : %s insert success' % (source, source_id))
					t_count += 1
				except Exception, e:
					self.debug_logger.debug('%s' % str(e))
					continue
			cur.close()
			obj.closeMysql(conn)
			return t_count
		except MySQLdb.Error, e:
			try:
				self.warn_logger.warn("Error %d:%s" % (e.args[0], e.args[1]))
				return 0
			except IndexError:
				self.warn_logger.warn("MySQL Error:%s" % str(e))
				return 0