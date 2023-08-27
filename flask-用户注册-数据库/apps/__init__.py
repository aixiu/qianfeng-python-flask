# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/24 11:33:01

from flask import Flask
import setting
from apps.user.view import user_bp  # 导入蓝图文件
from ext import db

def create_app():
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/')  # app是一个核心对象
    app.config.from_object(setting.DevelopmentConfig)  #加载配置
    
    # 初始化配置db
    db.init_app(app)  # 将db对象与app进行了关联
    
    # 蓝图
    app.register_blueprint(user_bp)  # 注册蓝图  此 user_bp
    
    
    # print(app.url_map)    
    return app