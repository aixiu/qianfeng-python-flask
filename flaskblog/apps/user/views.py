import os
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for, g
from sqlalchemy import and_, not_, or_
from apps.article.models import Article, Article_type
from apps.user.models import User, Photo   # 蓝图相关
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from apps.user.smssend import SmsSendAPIDemo
from werkzeug.utils import secure_filename
from setting import Config
from apps.utils.util import upload_qiniu

# 创建一个蓝图名为 user1 在当前文件定义就写 __name__  
# url_prefix='/user'  路由变为 http://127.0.0.1/user/XXXX
user_bp1 = Blueprint('user1', __name__, url_prefix='/user') 

required_login_list = ['/user/center', '/user/change', '/article/publish', '/user/upload_photo'] 

# ****重点*****
# 通过勾子函数来过滤指定页面，没登录则限制，有登录则放行
@user_bp1.before_app_request
def before_request():
    print('before_requestbefore_request', request.path)
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            return render_template('user/login1.html')
        else:
            user = User.query.get(id)
            # g对象，本次请求的对象
            g.user = user
            
@user_bp1.after_app_request
def after_request_test(response):
    response.set_cookie('a', 'bbbb', max_age=19)
    print('after_request_test')
    return response


@user_bp1.teardown_app_request
def teardown_request_test(response):
    print('teardown_request_test')
    return response

# 自定义过滤器  python3 字符串默认是Unicode编码，不再需要进行解码操作
@user_bp1.app_template_filter('cdecode')
def content_decode(content):
    # content = content.decode('utf-8')
    # if len(content) >= 200:
    #     return f'{content[:200]}......'
    # else:
        return f'{content}'

# 首页
@user_bp1.route('/')
def index():
    # 1、cookie获取方式
    # uid = request.cookies.get('uid', None)
    
    # 2、session的获取,session底层默认获取
    uid = session.get('uid')
    
    # 获取文章列表
    # articles = Article.query.order_by(Article.pdatetime.desc()).all()   # 默认是正序，  .asc()正序  .desc()倒序
    
    
    # 获取文章列表   7 6 5  |  4 3 2 | 1
    # 接收页码数
    page = int(request.args.get('page', 1))
    pagination = Article.query.order_by(Article.pdatetime.desc()).paginate(page=page, per_page=3)  # paginate分页， page 页码，per_page每页显示3篇
    
    print(pagination.items)  # [<Article 4>, <Article 3>, <Article 2>]
    print(pagination.page)  # 当前的页码数
    print(pagination.prev_num)  # 当前页的前一个页码数
    print(pagination.next_num)  # 当前页的后一页的页码数
    print(pagination.has_next)  # True  有没有上一页
    print(pagination.has_prev)  # True  有没有下一页
    print(pagination.pages)  # 总共有几页
    print(pagination.total)  # 总的记录条数

    # 获取分类列表
    types = Article_type.query.all()
    
    # 判断用户是否登录    
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user, types=types, pagination=pagination)
    else:
        return render_template('user/index.html', types=types, pagination=pagination)

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
        if f == '1':  # 用户名或者密码
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
        elif f == '2':  # 手机号码与验证码
            print('----->22222')
            phone = request.form.get('phone')
            code = request.form.get('code')
            # 先验证验证码
            valid_code = session.get(phone)
            print('valid_code:' + str(valid_code))
            if code == valid_code:
                # 查询数据库
                user = User.query.filter(User.phone == phone).first()
                print(user)
                if user:
                    # 登录成功
                    session['uid'] = user.id
                    return redirect(url_for('user1.index'))
                else:
                    return render_template('user/login1.html', msg='此号码未注册')
            else:
                return render_template('user/login1.html', msg='验证码有误！')
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
    # 补充验证手机号码是否注册，去数据库查询
    
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
    session[phone] = '189075'
    return jsonify(code=200, msg='短信发送成功！')

    # if ret is not None:
    #     if ret["code"] == 200:
    #         taskId = ret["result"]["taskId"]
    #         print("taskId = %s" % taskId)
    #         session[phone]='189075'
    #         return jsonify(code=200, msg='短信发送成功！')
    #     else:
    #         print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
    #         return jsonify(code=400, msg='短信发送失败！')
    
# 用户中心
@user_bp1.route('/center')
def user_center():
    types = Article_type.query.all()
    photos = Photo.query.filter(Photo.user_id == g.user.id).all()
    return render_template('user/center1.html', user=g.user, types=types, photos=photos)


# 图片的扩展名
ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp']

# 用户信息修改
@user_bp1.route('/change', methods=['GET', 'POST'])
def user_change():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        # 只要有文件（图片），获取方式必须使用request.files.get(name)
        icon = request.files.get('icon')
        # print('======>', icon)  # FileStorage
        # 属性： filename 用户获取文件的名字
        # 方法:  save(保存路径)
        icon_name = icon.filename  # 1440w.jpg
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name)  # 保证文件名是符合python的命名规则
            file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
            icon.save(file_path)
            # 保存成功
            
            user = g.user
            user.username = username
            user.phone = phone
            user.email = email
            path = 'upload/icon/' # 或是末尾一定要 /不然后边地加上 \ 否则显示 %5C  出错  或是用下边一行
            # user.icon = os.path.join(path, icon_name).replace('\\', '/')  # 把路径中的 \替换为 / 否则显示 %5C  出错
            user.icon = os.path.join(path, icon_name)
            db.session.commit()
            
            return redirect(url_for('user1.user_center'))
        else:
            return render_template('user/center1.html', user=g.user, msg='必须是扩展名是：jpg,png,gif,bmp格式')

        # 查询一下手机号码
        # users = User.query.all()
        # for user in users:
        #     if user.phone == phone:
        #         # 说明数据库中已经有人注册此号码
        #         return render_template('user/center.html', user=g.user,msg='此号码已被注册')
        #

    return render_template('user/center.html', user=g.user)


# 发表文章
@user_bp1.route('/article', methods=['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        type = request.form.get('type')
        content = request.form.get('content')
        print(title, type, content)

        return render_template('article/test.html', content=content)
    return '发表失败！'


# 上传照片
@user_bp1.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    # 获取上传的内容
    photo = request.files.get('photo')  # FileStorage
    # photo.filename, photo.save(path)
    # 工具模块中封装方法
    ret, info = upload_qiniu(photo)
    if info.status_code == 200:
        photo = Photo()
        photo.photo_name = ret['key']
        photo.user_id = g.user.id
        db.session.add(photo)
        db.session.commit()
        return '上传成功！'
    else:
        return '上传失败！'
    
    
@user_bp1.route('/myphoto')
def myphoto():
    page = int(request.args.get('page', 1))
    # 分页操作
    photos = Photo.query.paginate(page=page, per_page=2)
    user_id = session['uid']
    user = None
    if user_id:
        user = User.query.get(user_id)
    return render_template('user/myphoto.html', photos=photos, user=user)
    
    # photos = Photo.query.all()
    # return render_template('user/myphoto.html', photos=photos)