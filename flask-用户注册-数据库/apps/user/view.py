# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/23 22:15:37

from flask import Blueprint, redirect, render_template, request, url_for

from apps.user.model import User   # 蓝图相关
from ext import db

# 创建一个蓝图名为 user 在当前文件定义就写 __name__
user_bp = Blueprint('user', __name__)  

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userinfo = request.form.to_dict()
        if userinfo.get('password') ==  userinfo.get('repassword'):
            
            # 与模型结合
            # 1、找到模型类并创建对
            user = User()
            # 2、给对象的属性赋值
            user.username =  userinfo.get('username')
            user.password = userinfo.get('password')
            user.phone = userinfo.get('phone')
            
            # 添加数据  session缓存
            # 3、将 user 对象添加到 session中（类似缓存）
            db.session.add(user)
            # 4、提交数据
            db.session.commit()
            
            return '用户注册成功！' 
        else:
            return '两次密码不一致'

    return render_template('user/register.html')