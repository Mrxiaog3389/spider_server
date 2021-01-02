# -*- coding: utf-8 -*-
# @Time    : 2020/8/7 17:02
# @Author  : Xiaoyunlong


import configparser
import os,sys
import logging

def read_config():
    """
    读取配置
    :return: 返回配置对象
    """
    config = configparser.ConfigParser()  # 类实例化
    ini_path = os.getcwd() + '\\config.ini'
    config.read(ini_path)
    return config


class Init_Config(object):
    """
    初始化配置
    """
    def __init__(self):
        sys.path.append(os.getcwd())
        config = read_config()
        self.msqlserver = config['mysqldb']['msqlserver']
        self.msqdb = config['mysqldb']['msqdb']
        self.msqusername = config['mysqldb']['msqusername']
        self.msqpassword = config['mysqldb']['msqpassword']
        self.msqcoding = config['mysqldb']['msqcoding']
        self.rdsserver = config['redisdb']['rdsserver']
        self.rdspassword = config['redisdb']['rdspassword']
        self.logpath = os.getcwd() + '\\log\\' + config['log']['logfile']

    def init_log(self):
        log = logging.getLogger('django')
        return log