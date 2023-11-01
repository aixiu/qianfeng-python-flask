from flask import Blueprint, g, redirect, render_template, request, url_for
from apps.user.models import User
from apps.article.models import Article, Article_type
from exts import db

article_bp1 = Blueprint('article1', __name__, url_prefix='/article')

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