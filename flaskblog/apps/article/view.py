from flask import Blueprint, render_template, request
from apps.user.models import User
from apps.article.models import Article, Article_type
from exts import db

article_bp = Blueprint('article', __name__)

# 发布文章
@ article_bp.route('/publish', methods=['GET', 'POST'], endpoint='publish_article')
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        uid = request.form.get('uid')
        type_id = request.form.get('type')
        
        # 添加文章
        # 1、找到模型类并创建对
        article = Article()
        # 2、给对象的属性赋值
        article.title = title
        article.content =  content
        article.user_id = uid
        article.type_id = type_id
        # 添加数据  session缓存
        # 3、将 user 对象添加到 session中（类似缓存）
        db.session.add(article)
        # 4、提交数据
        db.session.commit()
        return '添加成功'
    else:
        users = User.query.filter(User.isdelete == False).all()
        article_type = Article_type.query.all()
        return render_template('article/add_article.html', users=users, article_type=article_type)
    
# 展示文章，根据文章找作者
@article_bp.route('/all')
def all_article():
    articles = Article.query.all()
    return render_template('article/all.html', articles=articles)

# 展示文章，根据作者找文章  http://127.0.0.1:5000/all1?id=1
@article_bp.route('/all1')
def all_article1():
    id = request.args.get('id')
    user = User.query.get(id)
    return render_template('article/all1.html', user=user)