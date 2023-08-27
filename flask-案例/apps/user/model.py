# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2022/11/23 22:49:18

class User:
    """在创建完对象之后 会自动调用, 它完成对象的初始化的功能"""
    def __init__(self, username, password, phone=None) -> None:
        self.username = username
        self.password = password
        self.phone = phone
        
    def __str__(self) -> str:
        """返回一个对象的描述信息"""
        return self.username