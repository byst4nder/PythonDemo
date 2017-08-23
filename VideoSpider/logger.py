# -*- coding: UTF-8 -*-
import glob
import logging
import logging.handlers

class Logger(object):
	def infoLogger(self):
		INFO_LOG_FILENAME = 'log/spider_INFO.log'
		info_logger = logging.getLogger('info_logger')
		info_logger.setLevel(logging.INFO)
		info_handler = logging.handlers.RotatingFileHandler(INFO_LOG_FILENAME, maxBytes=1024 * 1024, backupCount=10, )
		show_info_handler = logging.StreamHandler()
		info_logger.addHandler(info_handler)
		info_logger.addHandler(show_info_handler)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		info_handler.setFormatter(formatter)
		show_info_handler.setFormatter(formatter)
		return info_logger

	def debugLogger(self):
		DEBUG_LOG_FILENAME = 'log/spider_DEBUG.log'
		debug_logger = logging.getLogger('debug_logger')
		debug_logger.setLevel(logging.DEBUG)
		debug_handler = logging.handlers.RotatingFileHandler(DEBUG_LOG_FILENAME, maxBytes=1024 * 1024, backupCount=10, )
		show_debug_handler = logging.StreamHandler()
		debug_logger.addHandler(debug_handler)
		debug_logger.addHandler(show_debug_handler)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		debug_handler.setFormatter(formatter)
		show_debug_handler.setFormatter(formatter)
		return debug_logger

	def warnLogger(self):
		WARN_LOG_FILENAME = 'log/spider_WARN.log'
		warn_logger = logging.getLogger('warn_logger')
		warn_logger.setLevel(logging.WARNING)
		warn_handler = logging.handlers.RotatingFileHandler(WARN_LOG_FILENAME, maxBytes=1024 * 1024, backupCount=10, )
		show_warn_handler = logging.StreamHandler()
		warn_logger.addHandler(warn_handler)
		warn_logger.addHandler(show_warn_handler)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		warn_handler.setFormatter(formatter)
		show_warn_handler.setFormatter(formatter)
		return warn_logger