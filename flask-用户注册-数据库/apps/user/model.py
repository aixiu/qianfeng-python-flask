# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/23 22:49:18

from datetime import datetime
from ext import db

class User(db.Model):
    # db.Column(类型，约束) 映射表中的列
    '''
    类型 
    db.Integer        int
    db.String(15)     varchar(15)
    db.DateTime       datetime
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(20))   
     
    # 您不需要关心时间的位数，您可以使用strftime() method将日期和时间格式化为您想要的任何格式。例如，您可以像这样在模板中使用它：
    # {{ user.last_login_date.strftime('%Y-%m-%d %H:%M:%S') }}
    # 格式代码'%Y-%m-%d %H:%M:%S'将输出类似于'2020-12-30 14:05:16'的内容。检查所有可用的格式代码here的列表。
    # https://cloud.tencent.com/developer/ask/sof/1073229
    rdatetime = db.Column(db.DateTime, default=datetime.now)
    
    def __str__(self):
        return self.username
    
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String(20))
    gender = db.Column(db.Boolean, default=False)
    
    def __str__(self):
        return self.realname