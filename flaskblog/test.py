# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aixiu
# @Time  : 2023/11/02 09:20:54

# -*- coding: utf-8 -*-
# flake8: noqa

# from qiniu import Auth, put_file, etag
# import qiniu.config
# import os
# from setting import Config

# #需要填写你的 Access Key 和 Secret Key
# access_key = 'VSRtzMjvuLNBjt3mnVsYr68eacBsf-cGjVgGSPJK'
# secret_key = 'brmU6CUY_UBmOJi_iwQ7Ji_dU6YRhzlaGNiQnLpd'

# #构建鉴权对象
# q = Auth(access_key, secret_key)

# #要上传的空间
# bucket_name = 'flskblog'

# #上传后保存的文件名
# key = 'my-python-logo.png'

# #生成上传 Token，可以指定过期时间等
# token = q.upload_token(bucket_name, key, 3600)

# #要上传文件的本地路径
# localfile = os.path.join(Config.UPLOAD_ICON_DIR, 'QQ20211221222522.jpg')

# ret, info = put_file(token, key, localfile, version='v2') 
# print(info)
# print(ret)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)


import time
from datetime import datetime


filename = 'tupian.jpg'

# timeName = str(time.time()).split('.')[0]   # ==> tupian_1698977039.jpg
timeName = datetime.now().strftime('%Y%m%d%H%M%S')  # ==> tupian_20231103100539.jpg

suffix = filename.rsplit('.')[-1]
key = f"{filename.rsplit('.')[0]}_{timeName}.{suffix}"

print(key)

