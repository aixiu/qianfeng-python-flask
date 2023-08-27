# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/24 11:35:51

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps.user.model import User, UserInfo
from apps import create_app
from ext import db

# 加载蓝图 __init__.py 定义的 create_app  和 app = Flask(__name__) 一样
app = create_app()  # 创建APP对象

manager = Manager(app=app)

# 命令工具
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)


# 自定义命令，得使用 @manager.command  
@manager.command
def init():
    print('初始化')

if __name__ == '__main__':
    # python ./flask-用户更新/app.py runserver  运行
    manager.run()