# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2023/08/26 20:04:42

# 加密  md5  sha1  sha256  sha512

import hashlib

# 不可逆
msg =  'hello world'
md5 = hashlib.md5(msg.encode('utf-8'))
print(md5)  # 只是一个 hashlib 对象,要想打印出结果,得使用 .hexdigest()

r = md5.hexdigest()
print(r)  #32

sha1 = hashlib.sha1(msg.encode('utf-8')).hexdigest()
print(sha1)  # 40

sha256 = hashlib.sha256(msg.encode('utf-8')).hexdigest()
print(sha256)  #64

sha512 = hashlib.sha512(msg.encode('utf-8')).hexdigest()
print(sha512)  # 128