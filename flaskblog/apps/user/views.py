import hashlib
from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import and_, not_, or_
from apps.user.models import User   # 蓝图相关
from exts import db

# 创建一个蓝图名为 user1 在当前文件定义就写 __name__  
# url_prefix='/user'  路由变为 http://127.0.0.1/user/XXXX
user_bp1 = Blueprint('user1', __name__, url_prefix='/user')  

@user_bp1.route('/')
def index():
    return render_template('base.html')