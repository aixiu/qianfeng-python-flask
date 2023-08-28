from flask import Blueprint, render_template, request
from apps.user.models import User
from apps.article.models import Article
from exts import db

article_bp = Blueprint('article', __name__)

@ article_bp.route('/publish', methods=['GET', 'POST'], endpoint='publish_article')
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        uid = request.form.get('uid')
        
        # 添加文章
        # 1、找到模型类并创建对
        article = Article()
        # 2、给对象的属性赋值
        article.title = title
        article.content =  content
        article.user_id = uid
        # 添加数据  session缓存
        # 3、将 user 对象添加到 session中（类似缓存）
        db.session.add(article)
        # 4、提交数据
        db.session.commit()
        return '添加成功'
    else:
        users = User.query.filter(User.isdelete == False).all()
        return render_template('article/add_article.html', users=users)