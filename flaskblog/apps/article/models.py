from datetime import datetime
from exts import db

# 一对多关系 文档 http://www.pythondoc.com/flask-sqlalchemy/models.html#one-to-many
# flask_sqlalchemy数据库的外键与连接  https://blog.csdn.net/gaoke11240/article/details/120555953

'''
报错说明：
Article 表中已经有N条数据了，又在Article模型中新增加强一列，
此列是：type_id = db.Column(db.Integer, db.ForeignKey('ac_type.id'), nullable=False)  
注意：在这里添加了 nullable=False，说明不能为空。

问题就在于，我在已经存在的表中添加了一列而且要求此列数据不能为空，就是这个冲突的！！！
所以产生了错误。

解决办法：
nullable=False 不添加，就是充许为空
或者添加一个默认值也可以。
nullable=False  ===> default=1
'''

# 文章
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Text 长文本  Blob 二进制
    pdatetime = db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    save_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    
    #外键  左侧的建名必须参照右侧字符串所示的user.id里的内容存在才能建立 这个小写的user是数据库里边的表名不是模型类名！
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #这个是同步到数据库的，里边要存关系踺值的
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)  # __tablename__ = 'type' 这里定义了数据库别名 Article_type 为 type
    comments = db.relationship('Comment', backref='article')
    
# 文章分类
class Article_type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(20), nullable=False)
    articles = db.relationship('Article', backref='articletype')    
    
# 评论   
class Comment(db.Model):
    # 自定义表的名字
    __tablenname__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    cdatetime = db.Column(db.DateTime, default=datetime.now)
    
    def __str__(self):
        return self.comment