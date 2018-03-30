# -*- coding: utf-8 -*-

"""
log.py
~~~~~~~~~~~~~~~~~~~~

日志公共类初始化方法
不加参数则生成实例后自动记录console的内容
log_name: 日志名字
log_file: 日志文件
log_debug: True 开启调试，false 关闭调试

"""

import os
import logging

from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, log_name='', log_file='', log_debug=False):
        log_path = os.path.dirname(__file__).replace('app', 'log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self._log_debug = log_debug
        _format = '%(asctime)s %(levelname)s\n%(message)s\n'
        if log_name == '' and log_file == '':
            log_path = os.path.join(log_path, 'app_console.log')
            logging.basicConfig(level=logging.DEBUG,
                                format=_format,
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename=log_path,
                                filemode='a')
            formatter = logging.Formatter(_format)
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(formatter)
            self._logger = logging.getLogger('')
            self._logger.addHandler(console)
        else:
            log_file = os.path.join(log_path, log_file)
            self._logger = logging.getLogger(log_name)
            # handler = logging.FileHandler(filename=log_file)
            # 配置一个根据日期处理日志的handler，每天产生一个日志，可以保留10个
            handler = TimedRotatingFileHandler(filename=log_file,
                                               when='D',
                                               encoding='utf-8',
                                               interval=1,
                                               backupCount=10)
            formatter = logging.Formatter(_format)
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.DEBUG)

    def debug(self, msg):
        """
        debug 调试信息记录
        :param msg:
        :return:
        """
        if self._logger is not None:
            if self._log_debug:
                print('DEBUG:' + msg)
            self._logger.debug(msg)

    def info(self, msg):
        """
        info 正常信息记录
        :param msg:
        :return:
        """
        if self._logger is not None:
            self._logger.info(msg)

    def warning(self, msg):
        """
        warning 警告信息记录
        :param msg:
        :return:
        """
        if self._logger is not None:
            self._logger.warning(msg)

    def error(self, msg):
        """
        error 异常信息记录
        :param msg:
        :return:
        """
        if self._logger is not None:
            if self._log_debug:
                print('ERROR:' + msg)
            self._logger.error(msg)


slow_query_log = Logger('slow_query_log', 'slow_query_log.log')
