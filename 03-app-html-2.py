# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/21 13:32:10

import json
from flask import Flask, redirect, render_template, request, url_for, jsonify
import app_setting

users = []

app = Flask(__name__)
app.config.from_object(app_setting)
# app.config.from_pyfile('app_setting.py')


# 路由解析，通过用户访问的路径，匹配相应的函数
@app.route('/', endpoint='index')  # 映射一个字名叫 index,如：endpoint='index'
def index():
    return render_template('index-html-2.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.method)
    
    # POST:
    # request.form获得所有post参数放在一个类似dict类中,to_dict()是字典化
    # 单个参数可以通过request.form.to_dict().get("xxx","")获得
    # ----------------------------------------------------
    # GET:
    # request.args获得所有get参数放在一个类似dict类中,to_dict()是字典化
    # 单个参数可以通过request.args.to_dict().get('xxx',"")获得
        # ----------------------------------------------------
    # 原文链接：https://blog.csdn.net/u013055678/article/details/70214756/
    # https://www.jianshu.com/p/80950e5c773a


    
    # 第一种方法，request.form.get() 获取值
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     repassword = request.form.get('repassword')
    #     # 用户密码一致性验证
    #     if password == repassword:
    #         info = {
    #             'username': username,
    #             'password': password
    #         }
    #         # 保存用户信息
    #         users.append(info)
    #         return f'注册成功。{info}'
    #     else:
    #         return r'两次输出的密码不一致'
    
     # 第二种方法，request.form.to_dict() 获取值，如果是GET方法，可用 request.args.get()获取值
    if request.method == 'POST':
        # 获取用户信息    
        data = request.form.to_dict()        
        # 用户密码一致性验证
        if data.get('password') == data.get('repassword'):
            # 保存用户信息
            info = {
                'username': data.get('username'),
                'password': data.get('password')
            }
            users.append(info)
            # return f'注册成功。<a href="/">返回首页</a><br>'
            # return redirect('/', 301)   # 重定向，有两次响应，第一次是 301 + location（可以理解为 URL）, 第二次返回 location请求的地址内容，这里 location 就是 "/"
            return redirect(url_for('index'))  # 根据映射名找路径
        else:
            return r'两次输出的密码不一致'
        
        
    return render_template('register-1.html')

@app.route('/show')
def show():
    return json.dumps(users) # 无格式的
    # return jsonify(users)  # 有格式的

@app.route('/test')
def test():
    url = url_for('index')  # 路径或是路由的反向解析  映射
    print(url)  # '/'
    return 'test'
    


if __name__ == '__main__':
    app.run()