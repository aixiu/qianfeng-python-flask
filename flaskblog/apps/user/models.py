from datetime import datetime
from exts import db

'''
敲黑板:写完模型,得在启动文件导入 App.py导入该模型 User
'''

# 模型函数 User
class User(db.Model):
    # db.Column(类型，约束) 映射表中的列
    '''
    类型 
    db.Integer        int
    db.String(15)     varchar(15)
    db.DateTime       datetime
    unique 唯一
    nullable 不能为空
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(250), nullable=False)  # 要放加密后的长度 sha256
    phone = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(30))
    icon = db.Column(db.String(100))
    isdelete = db.Column(db.Boolean, default=False) # 逻辑删除用 默认 不删
    
    # 您不需要关心时间的位数，您可以使用strftime() method将日期和时间格式化为您想要的任何格式。例如，您可以像这样在模板中使用它：
    # {{ user.reatetime.strftime("%Y-%m-%d %H:%M:%S") }}
    # 格式代码'%Y-%m-%d %H:%M:%S'将输出类似于'2020-12-30 14:05:16'的内容。检查所有可用的格式代码here的列表。
    # https://cloud.tencent.com/developer/ask/sof/1073229
    rdatetime = db.Column(db.DateTime, default=datetime.now)
    
    #增加一个字段 ，以及反向引用
    articles = db.relationship('Article', backref ='user' )#这块是给模板用的，不在数据库里体现，但是模板里边可以引用   Article 模型名
    # relationship 是给模板使用的，ForeignKey是做映射使用的
    
    def __str__(self):
        return self.username
    

class Photo(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_name = db.Column(db.String(50), nullable=False)
    photo_datetime = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.photo_name