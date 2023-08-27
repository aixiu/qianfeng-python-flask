# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/23 21:44:34

from apps import create_app

# 加载蓝图 __init__.py 定义的 create_app  和 app = Flask(__name__) 一样
app = create_app()  

if __name__ == '__main__':
    app.run()