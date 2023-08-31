# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2023/08/26 19:29:02

from flask_migrate import Migrate
# from flask_script import Manager  # 高版本已不再使用
from apps.user.models import User  # 一定要导入模型模块
from apps.article.models import * # 一定要导入模型模块
from apps.goods.models import *
from apps import create_app
from exts import db

# 创建app对象
app = create_app()

# 使用命令管理 app对象  不再使用
# manager = Manager(app=app)

# 使用命令管理app和数据库操作之间的映射
migrate = Migrate(app=app, db=db)

# 添加命令 db  不再使用
# manager.add_command('db')

# 注意 ==> 新的执行命令
# https://www.jianshu.com/p/11ce08e078aa
# flask db init 、   flask db migrate、   flask db upgrade


#  运行命令 python ./app.py
if __name__ == '__main__':
    app.run()
    
    
# 一对多关系 文档 http://www.pythondoc.com/flask-sqlalchemy/models.html#one-to-many
# flask_sqlalchemy数据库的外键与连接  https://blog.csdn.net/gaoke11240/article/details/120555953
# Flask-SQLAlchemy外键及其关系  https://blog.csdn.net/qq_45112637/article/details/108383514