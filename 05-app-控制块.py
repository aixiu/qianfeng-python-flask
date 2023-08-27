# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/22 10:10:16

from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_pyfile('./app_setting.py')  # 导入配置文件


# 路由解析，通过用户访问的路径，匹配相应的函数
@app.route('/show1')
def show1():
    girls = ['张三', '李四', '王五', '赵六', '林如花', '孙凤姐',]
    users = [
        {'username': 'zhangsan', 'password': '123', 'addr': '湖北', 'phone': '13453247897'},
        {'username': 'zhangsan1', 'password': '333', 'addr': '西安', 'phone': '13453267897'},
        {'username': 'zhangsan2', 'password': '444', 'addr': '成都', 'phone': '13453267897'},
        {'username': 'zhangsan3', 'password': '125553', 'addr': '湖南', 'phone': '13453267897'},
    ]
    return render_template('show_控制块.html', girls=girls, users=users)


if __name__ == '__main__':
    app.run()