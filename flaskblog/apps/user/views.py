import hashlib
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from sqlalchemy import and_, not_, or_
from apps.user.models import User   # 蓝图相关
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash

# 创建一个蓝图名为 user1 在当前文件定义就写 __name__  
# url_prefix='/user'  路由变为 http://127.0.0.1/user/XXXX
user_bp1 = Blueprint('user1', __name__, url_prefix='/user')  

# 首页
@user_bp1.route('/')
def index():
    return render_template('user/index.html')

# 用户注册
@user_bp1.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userinfo = request.form.to_dict()
        if userinfo.get('password') ==  userinfo.get('repassword'):
            
            # 与模型结合
            # 1、找到模型类并创建对
            user = User()
            # 2、给对象的属性赋值
            user.username =  userinfo.get('username')
            user.password = generate_password_hash(userinfo.get('password'))  # 使用自带的函数方法 generate_password_hash 实现密码加密
            # user.password = hashlib.sha256(userinfo.get('password').encode('utf-8')).hexdigest()  # 密码加密
            user.phone = userinfo.get('phone')
            user.email = userinfo.get('email')
            
            # 添加数据  session缓存
            # 3、将 user 对象添加到 session中（类似缓存）
            db.session.add(user)
            # 4、提交数据
            db.session.commit()
            
            return redirect(url_for('user.index'))
        else:
            return '两次密码不一致'
    return render_template('user/register1.html')

# 手机号码验证
@user_bp1.route('/checkphone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    print(user)
    # code: 400 不能用    200 可以用
    if len(user) > 0:
        return jsonify(code=400, msg='此号码已被注册')
    else:
        return jsonify(code=200, msg='此号码可用')
    
# 用户登录
@user_bp1.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userinfo = request.form.to_dict()        
        # 查询 在数据库里找 在键名为 username 里找 叫userinfo.get('username')的对象
        user_list = User.query.filter_by(username=userinfo.get('username'))
        for u in user_list:
            # 此时的u表示的就是用户对象
            # 如果flag=True表示匹配，否则密码不匹配
            flag = check_password_hash(User.password, userinfo.get('password'))
            if flag:
                return '用户登录成功'
        else:
            return render_template('user/login1.html', msg='用户名或者密码有误')
    return render_template('user/login1.html')