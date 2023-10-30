import hashlib
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import and_, not_, or_
from apps.user.models import User   # 蓝图相关
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from apps.user.smssend import SmsSendAPIDemo

# 创建一个蓝图名为 user1 在当前文件定义就写 __name__  
# url_prefix='/user'  路由变为 http://127.0.0.1/user/XXXX
user_bp1 = Blueprint('user1', __name__, url_prefix='/user')  

# 首页
@user_bp1.route('/')
def index():
    # 1、cookie获取方式
    # uid = request.cookies.get('uid', None)
    
    # 2、session的获取,session底层默认获取
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user)
    else:
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
            
            return redirect(url_for('user1.index'))
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
        f = request.args.get('f')
        if f == 1:  # 用户名或者密码
            userinfo = request.form.to_dict()        
            # 查询 在数据库里找 在键名为 username 里找 叫userinfo.get('username')的对象
            user_list = User.query.filter_by(username=userinfo.get('username'))
            for u in user_list:
                # 此时的u表示的就是用户对象
                # 如果flag=True表示匹配，否则密码不匹配
                flag = check_password_hash(u.password, userinfo.get('password'))
                if flag:
                    # 1。cookie实现机制
                    # response = redirect(url_for('user1.index'))
                    # response.set_cookie('uid', str(u.id), max_age=1800)
                    # return response
                    # 2。session机制,session当成字典使用
                    session['uid'] = u.id
                    return redirect(url_for('user1.index'))
            else:
                return render_template('user/login1.html', msg='用户名或者密码有误')
        elif f == 2:  # 手机号码与验证码
            pass
    return render_template('user/login1.html')

# 用户退出
@user_bp1.route('/logout')
def logout():
    # 1。 cookie的方式
    # response = redirect(url_for('user.index'))
    # 通过response对象的delete_cookie(key),key就是要删除的cookie的key
    # response.delete_cookie('uid')
    # return response
    
    # 2。session的方式
    # del session['uid']
    session.clear()
    return redirect(url_for('user1.index'))

# 发送短信息
@user_bp1.route('/sendMsg')
def send_message():
    phone = request.args.get('phone')
    SECRET_ID = "dcc535cbfaefa2a24c1e6610035b6586"  # 产品密钥ID，产品标识
    SECRET_KEY = "d28f0ec3bf468baa7a16c16c9474889e"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "748c53c3a363412fa963ed3c1b795c65"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
    params = {
        "mobile": phone,
        "templateId": "10084",
        "paramType": "json",
        "params": "json格式字符串"
    }
    ret = api.send(params)
    print(ret)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["result"]["taskId"]
            print("taskId = %s" % taskId)            
        else:
            print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))