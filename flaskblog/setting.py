# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/24 11:31:18


# APP配置文件

# 一些配置文件
class Config:    
    DEBUG = True
    # mysql+pymysql(驱动)://user:password@hostip:port/databasename
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flask-user'
    # 配置 SQLite 数据库, 默认存放在 app instance 文件夹下 
    # 原文：https://www.bilibili.com/read/cv24640972/    https://zhuanlan.zhihu.com/p/54017111
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask-blog.db'#设置数据库URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
class DevelopmentConfig(Config):
    ENV = 'development'
    
class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    
    
    