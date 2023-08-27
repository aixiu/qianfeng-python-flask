# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/23 00:31:00

from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('./app_setting.py')

@app.route('/')
def index():
    return render_template('index.html')

# 路由解析，通过用户访问的路径，匹配相应的函数
@app.route('/base')
def load_base():
    return render_template('base-模板继承.html')

@app.route('/welocme')
def welocme():
    return render_template('welcome.html')

@app.route('/macro')
def use_macro():
    return render_template('macro/macro-宏.html')

@app.route('/macro1')
def use_macro1():
    return render_template('macro/macro-宏-1.html')




if __name__ == '__main__':
    print(app.url_map)  # 查看所有路由
    app.run()