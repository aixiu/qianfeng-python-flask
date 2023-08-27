# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/22 00:40:28

from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_pyfile('./app_setting.py')

class Girl:
    def __init__(self, name, addr) -> None:
        self.name = name
        self.gender = '女'
        self.addr = addr
        
    def __str__(self) -> str:
        return self.name


# 路由解析，通过用户访问的路径，匹配相应的函数
@app.route('/show')
def hello_world():
    name = '量子广告'
    age = 18
    friends = ["张三", "李四", "王二麻子", "赵五"]
    dict1 = {'gift': '大手镯', 'gift1':'鲜花'}
    
    # 创建对象
    girlfriend = Girl('美美', '湖北')
    return render_template('show.html', name=name, age=age, gender='男', friends= friends, dict1=dict1, girl=girlfriend)
    # 如果模板没找到传递的变量，则以空白字符串显示 


if __name__ == '__main__':
    app.run()