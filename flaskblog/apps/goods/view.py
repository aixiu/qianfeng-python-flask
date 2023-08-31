from flask import Blueprint, render_template, request
from apps.user.models import User
from apps.goods.models import Goods, User_goods
from exts import db

goods_bp = Blueprint('goods', __name__)

# 根据用户找商品  (XXX买了哪些商品)
@goods_bp.route('/findgoods')
def find_goods():
    user_id = request.args.get('uid')
    user = User.query.get(user_id)
    return render_template('goods/findgoods.html', user=user)

# 根据商品找用户 (xxx商品哪些人买了)
@goods_bp.route('/finduser')
def find_user():
    goods_id = request.args.get('gid')
    goods = Goods.query.get(goods_id)  # 根据 goods_id找商品对象
    return render_template('goods/finduser.html', goods=goods)

# 添加购买记录  (用户买商品)
@goods_bp.route('/show')
def show():
    users = User.query.filter(User.isdelete==False).all()
    goods_list = Goods.query.all()
    return render_template('goods/show.html', users=users, goods_list=goods_list)

@goods_bp.route('/buy')
def buy():
    uid = request.args.get('uid')
    gid = request.args.get('gid')
    ug = User_goods()
    ug.user_id = uid
    ug.goods_id = gid
    
    db.session.add(ug)
    db.session.commit()
    
    return '购买成功'