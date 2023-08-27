# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/23 22:15:37

from flask import Blueprint, redirect, render_template, request

from apps.user.model import User   # 蓝图相关

# 创建一个蓝图名为 user 在当前文件定义就写 __name__
user_bp = Blueprint('user', __name__)  

# 列表保存的是一个一个的用户对象
users = []

@user_bp.route('/')
def user_center():
    return render_template('user/show.html', users=users)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获取 post 提交的数据
        user_data = request.form.to_dict()
        # 用户密码一致性验证
        if user_data.get('password') == user_data.get('repassword'):
            # 用户名唯一   还可以用集合方式
            for user_info in users:
                if user_info.username == user_data.get('username4'):
                    return render_template('user/register.html', msg='用户名已存在')                
            # 创建 user 对象
            user_info = User(user_data.get('username'), user_data.get('password'), user_data.get('phone'))
            # 添加用户对象到用户列表
            users.append(user_info)
            return redirect('/')
            
    return render_template('user/register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def longin():
    return '用户登录'

@user_bp.route('/del')
def del_user():
    # 获取传递的 username  
    # show.html页页传递过来的 username  location.href = '/del?username=' + username
    del_username = request.args.get('username')
    
    # 根据 username 找到列表中的 user 对象
    for user in users:
        if user.username == del_username:
            # 删除 user
            users.remove(user)
            # return f'删除成功 --> {del_username}'
            return redirect('/')  # 重定向到 / 首页页面
    else:
        return '删除失败'
    
    
@user_bp.route('/update', methods=['GET', 'POST'], endpoint='update')
def update_user():
    if request.method == 'POST':
        # 方法一
        userinfo = request.form.to_dict()
        for user in users:
            if user.username == userinfo.get('realname'):
                user.usrname = userinfo.get('username')
                # user.password = userinfo.get('password')
                user.phone = userinfo.get('phone')
                return '更改成功'
        
        # 方法二
        # realname = request.form.get('realname')
        # username = request.form.get('username')
        # password = request.form.get('password')
        # phone = request.form.get('phone')
        # for user in users:
        #     if user.username == realname:
        #         user.usrname = username
        #         # user.password = password
        #         user.phone = phone
        #         return '更改成功'
        
    else:
        # get请求
        dl_username = request.args.get('username')
        for user in users:
            if user.username == dl_username:
                return render_template('user/update.html', user=user)
    
    

@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    return '用户退出'