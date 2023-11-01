from flask import Blueprint, g, jsonify, redirect, render_template, request, url_for
from apps.user.models import User
from apps.article.models import Article, Article_type
from exts import db

article_bp1 = Blueprint('article1', __name__, url_prefix='/article')


# 自定义过滤器  python3 字符串默认是Unicode编码，不再需要进行解码操作
@article_bp1.app_template_filter('cdecode')
def content_decode(content):
    # content = content.decode('utf-8')
    return f'{content}'

# 添加文章
@article_bp1.route('/publish', methods=['POST', 'GET'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        type_id = request.form.get('type')
        content =  request.form.get('content') 
        
        # 添加文章
        article = Article()
        article.title = title
        article.type_id = type_id
        article.content = content
        article.user_id = g.user.id
        
        db.session.add(article)
        db.session.commit()
        
        return redirect(url_for('user1.index'))
    
@article_bp1.route('/detail')
def article_detail():
    # 获取文章对象通过id
    article_id = request.args.get('aid')
    article = Article.query.get(article_id)
    # 获取文章分类
    types = Article_type.query.all()

    return render_template('article/detail.html', article=article, types=types)

@article_bp1.route('/love')
def article_love():
    article_id = request.args.get('aid')
    tag = request.args.get('tag')

    article = Article.query.get(article_id)
    if tag == '1':
        article.love_num -= 1
    else:
        article.love_num += 1
    db.session.commit()
    return jsonify(num=article.love_num)