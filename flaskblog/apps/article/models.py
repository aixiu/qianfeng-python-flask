from datetime import datetime
from exts import db

# 一对多关系 文档 http://www.pythondoc.com/flask-sqlalchemy/models.html#one-to-many
# flask_sqlalchemy数据库的外键与连接  https://blog.csdn.net/gaoke11240/article/details/120555953
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Text 长文本
    pdatetime = db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    save_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    
    #外键  左侧的建名必须参照右侧字符串所示的user.id里的内容存在才能建立 这个小写的user是数据库里边的表名不是模型类名！
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #这个是同步到数据库的，里边要存关系踺值的
    
    
    
    
    