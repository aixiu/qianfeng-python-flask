import hashlib
from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import and_, not_, or_
from apps.user.models import User   # 蓝图相关
from exts import db

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
            user.password = hashlib.sha256(userinfo.get('password').encode('utf-8')).hexdigest()  # 密码加密
            user.phone = userinfo.get('phone')
            
            # 添加数据  session缓存
            # 3、将 user 对象添加到 session中（类似缓存）
            db.session.add(user)
            # 4、提交数据
            db.session.commit()
            
            return redirect(url_for('user.user_center'))
        else:
            return '两次密码不一致'

    return render_template('user/register.html')


@user_bp.route('/')
def user_center():
    # 查询数据库中的数据
    users = User.query.all()  # select * from user;
    print(users)  # [<User 1>, <User 2>] 用户对像列表
    return render_template('user/center.html', users=users)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userinfo = request.form.to_dict()
        # 关键 select * from user where username 查找用户名或密码
        new_password = hashlib.sha256(userinfo.get('password').encode('utf-8')).hexdigest()
        # 查询 在数据库里找 在键名为 username 里找 叫userinfo.get('username')的对象
        user_list = User.query.filter_by(username=userinfo.get('username'))
        print(user_list)
        for u in user_list:
            # 此时的u表示的就是用户对象
            if u.password == new_password:
                return '用户登录成功'
        else:
            return render_template('user/login.html', msg='用户名或者密码有误')
    return render_template('user/login.html')

'''
--------username
--------password
    登录
提交过来的  username +  password

跟数据库中的数据进行匹配
'''
@user_bp.route('/test')
def test():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    print(user.username, user.phone, user.reatetime)
    
    # user = User.query.filter_by(username=username).last()  #  没有last取值方法
    # print(user.username, user.reatetime)
    
    return 'test'
# http://127.0.0.1:5000/test?username=aixiu

@user_bp.route('/select')
def user_select():
    user = User.query.get(4) # 根据主键查询用户 使用get(主键值) 返回值是一个用户对象
    user1 = User.query.filter(User.username =='aixiu').first() # aixiu 对象
    # user1 = User.query.filter(User.username =='aixiu').all()  # [<User 4>]
    
    user_list = User.query.filter(User.username.startswith('z')).all()
    # select * from user where username like 'z%';
    user_list1 = User.query.filter(User.username.contains('g')).all()
    user_list2 = User.query.filter(User.username.like('a%')).all()
    
    user_list3 = User.query.filter(or_(User.username.like('a%'), User.username.contains('i'))).all()
    # select * from user where username like 'a%' or username like ('%i%')
    
    # user_list4 = User.query.filter(and_(User.username.contains('i'), User.reatetime <'2023-08-26 23:21:27'))
    user_list4 = User.query.filter(and_(User.username.contains('g'), User.reatetime.__lt__('2023-08-26 23:21:27'))).all()
    # select * from user where username like '%g%' and reatetime < 'xxx'
    # __lt__ 之前，  __gt__ 之后
    user_list5 = User.query.filter(not_(User.username.contains('g'))).all()
    
    user_list6 = User.query.filter(User.phone.in_(['15901658763', '13597881770'])).all()
    
    # 排序
    user_list7 = User.query.filter(User.username.contains('i')).order_by('reatetime').all()
    # 排序 降序
    user_list8 = User.query.order_by(-User.id).all()    
    user_list9 = User.query.filter(User.username.contains('g')).order_by(-User.reatetime).all()
    
    # 限制 limit + offset
    user_list10 = User.query.limit(2).all()  # 默认获取两条
    # 如果拿3.4 得用 offset(2).limit(2) 跳过（偏移）两个记录再取两个记录
    user_list11 = User.query.offset(2).limit(2).all()
    
    
    
    
    
    return render_template('user/select.html', user=user, user1=user1, users=user_list, user_list1=user_list1, user_list2=user_list2, user_list3=user_list3, user_list4=user_list4, user_list5=user_list5, user_list6=user_list6, user_list7=user_list7, user_list8=user_list8, user_list9=user_list9, user_list10=user_list10, user_list11=user_list11)
