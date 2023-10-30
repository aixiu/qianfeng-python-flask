模板和模型的参照：
https://jinja.palletsprojects.com/en/2.11.x/templates/#super-bLocks
https://jinja.palletsprojects.com/en/3.0.x/templates/#super-bLocks

1、查询
查询所有： 模型类.query.all()   ==> select * from user;

有条件的查询： 
    模型类.query.filter_by(字段名 = 值)   ==> select * from user where 字段=值;
    模型类.query.filter_by(字段名 = 值).first()   ==> select * from user where 字段=值 limit..;

select * from user where age>17 and gender='男';
select * from user where username like 'zhang%';
select * from user where rdatetime > xxx and rdatetime < xxx;

模型类.query.filter()  里面是布尔的条件 模型类.query.filter(模型名.字段名 == '值')
模型类.query.filter_by()  里面是一个等值 模型类.query.filter_by(字段名 = 值)


user1 = User.query.filter(User.username =='aixiu').first() # aixiu 对象
user1 = User.query.filter(User.username =='aixiu').all()  # [<User 4>]

**** 模型类.query.filter() ****
1、模型类.query.filter().all()  ==> 列表
2、模型类.query.filter().first()  ==> 对象
3、User.query.filter(User.username.endswith('z')).all() ==>  select * from user where username like '%z';
4、User.query.filter(User.username.startswith('z')).all()  ==>  select * from user where username like 'z%';
5、User.query.filter(User.username.contains('z')).all()  ==>  select * from user where username like '%z%';
6、user_list2 = User.query.filter(User.username.like('a%')).all()

多条件：
from sqlalchemy import and_, or_, not_
并且： and_  或者：or_  非：not_  
User.query.filter(or_(User.username.like('a%'), User.username.contains('i'))).all()
# select * from user where username like 'a%' or username like ('%i%')

User.query.filter(and_(User.username.contains('g'), User.reatetime.__lt__('2023-08-26 23:21:27'))).all()
# select * from user where username like '%g%' and reatetime < 'xxx'

and or order_by like ... 等查询语句

User.query.filter(not_(User.username.contains('g'))).all()  -- 取返 not_

18 19 20 17 21 22 
select * from where age in [17, 18, 20, 22]
User.query.filter(User.phone.in_(['15901658763', '13597881770'])).all()  查找指定的用 in_


补充：__gt__--大于, __lt__--小于, __ge__(gt equal)--大于等于, __le__(le equal)--小于等于   ==> 通常应用在一范围（整型，日期） 也可能直接使用  >, <, >=, <=, !=

排序： order_by
user_list7 = User.query.filter(User.username.contains('i')).order_by('reatetime').all()

# 排序 降序

user_list8 = User.query.order_by(-User.id).all()    对所有的进行排序
user_list9 = User.query.filter(User.username.contains('g')).order_by(-User.reatetime).all()  选筛选再排序

注意： order_by(参数)：
1、直接是字符串："字段名" 但是不能倒序
2、填字段名：  模型.字段名 order_by(模型.字段名)   倒序 -模型.字段名  order_by(-模型.字段名)

限制： limit 

如果有50条记录，10条显示一页就要用 limit限制

# 限制 limit + offset
    user_list10 = User.query.limit(2).all()  # 默认获取两条
    # 如果拿3.4 得用 offset(2).limit(2) 跳过（偏移）两个记录再取两个记录
    user_list11 = User.query.offset(2).limit(2).all()


总结：
1、User.query.all()  所有
2、User.query.get(主键名)  一个
3、User.query.filter()  * 重点
    如果要检索的字段是字符串(varchar, db.String):
        User.username.startswith('')
        User.username.endswith('')
        User.username.contains('')
        User.username.like('')
        User.username.in_('['', '', '']')
        User.username == 'xxxx'
    如果要检索的字段是整型或者日期类型：
        User.age.__lt__(18)
        User.reatetime.__gt__('.....')
        User.age.__le__(18)
        User.age.__ge__(18)
        User.age.between(15, 30)  15-30之间
    多个条件一起检索：
        and_, or_
    非的条件：
        not_
    排序：
        order_by()
    获取指定数量：
        limit().offset()
4、User.query.filter_by()

两种删除
1、逻辑删除( 定应急数据库中的表的时候，添加一个字段 isdelete, 通过此字段控制是否删除)
id = request.args.get(id)
user = User.query.get(id)
user.isdelete = True
db.session.commit()

2、物理删除(彻底从数据库中删掉)
id = request.args.get(id)
user = User.query.get(id)
db.session.delete(user)
db.session.commit()


更新
id = request.args.get(id)
user = User.query.get(id)
# 修改对象的属性
user.username = xxx
user.phone = xxx
# 提交更改
db.session.commit()


'''python
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary='Page_tag', backref='pages')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class Page_tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db.Column('tag_id', db.Integer, db.Foreignkey('tag.id))
    db.Column('page_id', db.Integer, db.Foreignkey('page.id))


'''



尝分析：

电影订票网站中：电影与用户的关系
电影 goods   user

class User(db.Model):
    xxxx
    articles = db.relationship('Article', backref='user')


# Foreignkey 加到一对多，多的这张表,一句话，在多上加外键，关联
class Article(db.Model)
    xxxx
    user_id = db.Column(db.Integer, db.Foreignkey('user.id'))
    # user = db.relationship('User', backref='article')


----模板
    --html
    --js
    --css 
    --images

使用flask-bootstrap:
步骤：
1、pip install flask-bootstrap
2、进行配置： 
    在：exts\__init__.py 中
    from flask_bootstrap import Bootstrap
    bootstrap = Bootstrap()

    在：apps\__init__.py 中
    # 初始化bootstrap
    bootstrap.init_app(app=app)
3、使用：
    内置的block

    {% extends "bootstrap/base.html" %}
    {% block title %}首页{% endblock %}

    {% block navbar %} {% endblock %}

    {% block content %} {% endblock %}

    {% block styles %}  {% endblock %}
    {% block head %} {% endblock %}
    {% block body %} {% endblock %}


密码加密：
注册：
generate_password_hash(password)  ----> 加密后的密码
sha256加密$salt$48783748uhr8738478473...

登录：
check_password_hash(数据库获取的密码（已加密）,原始密码)  -----> bool:False,True
check_password_hash(pwdHash,password)  -----> bool:False,True


会话机制：
1。cookie方式：

  保存：
    通过response对象保存。
    response = redirect(xxx)
    response = render_template(xxx)
    response = Response()
    response = make_response()
    response = jsonify()
    # 通过对象调用方法
    response.set_cookie(key,value,max_age)
    其中max_age表示过期时间，单位是秒
    也可以使用expires设置过期时间，expires=datetime.now()+timedelta(hour=1)

  获取：
    通过request对象获取。
    request.form.get()
    request.args.get()
    cookie也在request对象中
    request.cookies.get(key) ----> value

  删除：
     通过response对象删除。 把浏览器中的key=value删除了
    response = redirect(xxx)
    response = render_template(xxx)
    response = Response()
    response = make_response()
    response = jsonify()
    # 通过对象调用方法
    response.delete_cookie(key)

2。session：  是在服务器端进行用户信息的保存。一个字典
注意：
使用session必须要设置配置文件，在配置文件中添加SECRET_KEY='xxxxx'，
添加SECRET_KEY的目的就是用于sessionid的加密。如果不设置会报错。

  设置：
    如果要使用session，需要直接导入：
    from flask import session

    把session当成字典使用，因此：session[key]=value
    就会将key=value保存到session的内存空间
    **** 并会在响应的时候自动在response中自动添加有一个cookie：session=加密后的id ****
  获取
     用户请求页面的时候就会携带上次保存在客户端浏览器的cookie值，其中包含session=加密后的id
     获取session值的话通过session直接获取，因为session是一个字典，就可以采用字典的方式获取即可。
     value = session[key] 或者 value = session.get(key)
     这个时候大家可能会考虑携带的cookie怎么用的？？？？
     其实是如果使用session获取内容,底层会自动获取cookie中的sessionid值，
     进行查找并找到对应的session空间

   删除
    session.clear()  删除session的内存空间和删除cookie
    del session[key]  只会删除session中的这个键值对，不会删除session空间和cookie

businessId
