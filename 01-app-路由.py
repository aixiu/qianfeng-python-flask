# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/20 10:55:56

from flask import Flask
import app_setting

app =  Flask(__name__)

# print(app.config)
app.config.from_object(app_setting)

data = {
    "a": "郧西",
    "b": "十堰",
    "c": "武汉"    
}

@app.route('/')
def index():
    return '欢迎大家'

@app.route('/city/<name>')
def city(name):
    # return data[name]
    return data.get(name)

@app.route('/add/<int:num>')
def add(num):
    print(f'Num ---> {type(num)}')
    result = num + 10
    return str(result)

@app.route('/add1/<float:money>')
def add1(money):
    print((f'money ---> {type(money)}'))
    return str(money)

@app.route('/index/<path:p>')
def git_path(p):
    print(f'P ---> {type(p)}')
    print(p)
    
    return p


''''
基于MAC地址，时间戳，随机数来生成唯一的uuid，可以保证全球范围内的唯一性。
print(uuid.uuid1())
通过伪随机数得到uuid，是有一定概率重复的 
print(uuid.uuid4())

'''

import uuid
for i in range(10):
    doc_name = uuid.uuid1().hex  # .hex意在去除uuid中的横杠（-）
    print(doc_name)

@app.route(f'/text/<uuid:uid>')
def text(uid):
    print(f'ID ---> {type(uid)}')        
    return f'获取唯一的标识码 ==> {uid}'





if __name__ == '__main__':

    app.run(port=8080)
