from flask import Flask
from setting import DevelopmentConfig
from exts import db
from apps.user.view import user_bp
from apps.user.views import user_bp1
from apps.article.view import article_bp
from apps.article.views import article_bp1
from apps.goods.view import goods_bp
from exts import bootstrap


def create_app():
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
    app.config.from_object(DevelopmentConfig)
    
    # 初始化db
    db.init_app(app=app)
    
    # 初始化bootstrap
    bootstrap.init_app(app=app)
    
    # 注册蓝图
    app.register_blueprint(user_bp)  # 用户蓝图
    app.register_blueprint(user_bp1)  # 博客用户蓝图
    app.register_blueprint(article_bp)  # 文章蓝图
    app.register_blueprint(article_bp1)  # 文章蓝图
    app.register_blueprint(goods_bp)  # 购买商品蓝图
    
    # 调试用，打印所有路由
    # print(app.url_map)
    
    return app