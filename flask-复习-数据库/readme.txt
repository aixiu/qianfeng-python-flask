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
4、User.query.filter_by()

