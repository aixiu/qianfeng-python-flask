from exts import db


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __str__(self):
        return self.gname


# tags = db.Table('tags',   # 表名
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),  # 列名tag_id ，主键参考 tag.id
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id')),# page_id ，主键参考 page.id
# )


# 关系表 承接的是 user和goods之间的关系
class User_goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user表的id  表名也就是 class User(db.Model) 函数名，生成数据表后就是小写的了
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    # goods表的id 表名也就是 class Goods(db.Model) 函数名，生成数据表后就是小写的了
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id')) 
    number = db.Column(db.Integer, default=1)
