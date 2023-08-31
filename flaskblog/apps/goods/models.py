from exts import db


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gname = db.Column(db.String(100), nullable=False)  # 商品名
    price = db.Column(db.Float, nullable=False)  # 价格
    users = db.relationship('User', backref='goodslist', secondary='user_goods') 
    # 因为goods表和user表没有直接外键，所以用参数secondary='user_goods'意思就是，如果要通过goods表找user 可以通过user_goods找，因为 user_goods表和user表有外键关系，（意思就是去第三方的表里去找）
    # 模型名 User  secondary='user_goods'=号后是表名
    # backref ==> back reference 反向查找

    def __str__(self):
        return self.gname


# tags = db.Table('User_goods',   # 表名
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),  # user_id ，主键参考 user.id
#     db.Column('goods_id', db.Integer, db.ForeignKey('goods.id')) # goods_id ，主键参考 goods.id
#     db.Column('number', default=1)  # 字段


# 关系表 承接的是 user和goods之间的关系
class User_goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user表的id  表名也就是 class User(db.Model) 函数名，生成数据表后就是小写的了
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    # goods表的id 表名也就是 class Goods(db.Model) 函数名，生成数据表后就是小写的了
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id')) 
    number = db.Column(db.Integer, default=1)
