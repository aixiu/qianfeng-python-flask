# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/20 23:43:07

# app.py 与 模板的结使用

from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_pyfile('./app_setting.py')

@app.route('/register')
def register():
    r = render_template('register.html')
    return r

@app.route('/register2', methods=['GET', 'POST'])
def register2():
    print(request.full_path)  # /register2?username=aixiu&address=shendl
    print(request.path)  # /register2
    
    # GET 请求方法
    # print(request.args)  # ImmutableMultiDict([('username', 'aixiu'), ('address', 'shendlax')])  可以看成是字典  只能获取 GET请求的
    # username = request.args.get('username')  # GET请求，可以此法取值
    # address = request.args.get('address')  # GET请求，可以此法取值
    # print(username)
    # print(address)
    
    # POST 请求方法
    print('====', request.data)
    print('====', request.date)
    print(request.form)  # 如果请求方法是post则需要通过 request.form 方法取值
    username=request.form.get('username')
    address = request.form.get('address')
    print(username)
    print(address)
    
    return f'登录成功 ==> 用户名：{username} | 地址：{address}' 
    
if __name__ == '__main__':
    print(app.url_map)  # 路由规则
    app.run()
