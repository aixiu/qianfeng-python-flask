# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/20 11:09:52

# APP配置文件

# 一些配置文件
ENV = 'development'
DEBUG = True

# 解决浏览器中json数据，中文无法展示的问题
JSON_AS_ASCII = False   # 中文正常化，解决乱码
JSON_SORT_KEYS = False   # json不排序
JSONIFY_PRETTYPRINT_REGULAR = True  # 输出json格式化完美显示
JSONIFY_MIMETYPE = "application/json;charset=utf-8"   # 指定浏览器渲染的文件类型，和解码格式；