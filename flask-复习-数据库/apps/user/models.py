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
    password = db.Column(db.String(64), nullable=False)  # 要放加密后的长度 sha256
    phone = db.Column(db.String(11), unique=True)
    isdelete = db.Column(db.Boolean, default=False) # 逻辑删除用 默认 不删
    
    # 您不需要关心时间的位数，您可以使用strftime() method将日期和时间格式化为您想要的任何格式。例如，您可以像这样在模板中使用它：
    # {{ user.reatetime.strftime("%Y-%m-%d %H:%M:%S") }}
    # 格式代码'%Y-%m-%d %H:%M:%S'将输出类似于'2020-12-30 14:05:16'的内容。检查所有可用的格式代码here的列表。
    # https://cloud.tencent.com/developer/ask/sof/1073229
    reatetime = db.Column(db.DateTime, default=datetime.now)
    
    def __str__(self):
        return self.username