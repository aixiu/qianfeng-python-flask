# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/24 11:31:18

import os

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
    # secret_key
    SECRET_KEY = 'aixiu_shendlax'
    
    # 项目路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 静态文件夹的路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    # 头像的上传目录
    UPLOAD_ICON_DIR = os.path.join(STATIC_DIR, 'upload/icon')
    # 相册的上传目录
    UPLOAD_PHOTO_DIR = os.path.join(STATIC_DIR, 'upload/photo')
    
class DevelopmentConfig(Config):
    ENV = 'development'
    
class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    
    
if __name__ == '__main__':
    print(Config.BASE_DIR)
    # print(os.path.abspath(__file__))
    print(Config.STATIC_DIR)
    print(Config.UPLOAD_ICON_DIR) 
    print(Config.UPLOAD_PHOTO_DIR) 