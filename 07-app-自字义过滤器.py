# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/22 23:13:06

from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('./app_setting.py')


# 路由解析，通过用户访问的路径，匹配相应的函数
@app.route('/')
def index():
    msg = 'hello vevryone hello world'
    li = [2, 3, 9, 7, 5, 6]
    return render_template('define_filter-自定义过滤器.html', msg=msg, li=li)

# 第一种方式
# 过滤器本质就是函数
def replace_hello(value):
    print(f'---> {value}')
    value = value.replace('hello', '')
    print(f'---> {value}')
    return value.strip()  # 将替换的结果返回

app.add_template_filter(replace_hello, 'replace')

# 第二种方式
# 用装饰器
@app.template_filter('listreverse')
def reverse_list(li):
    temp_li = list(li)
    temp_li.reverse()
    return temp_li




if __name__ == '__main__':
    app.run()