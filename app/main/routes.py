from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.main import bp
from app.models import Post 


@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False) 
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None 

    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/resume')
def resume():
    return "put resume here"

@bp.route('/about')
def about():
    return "put about here"

    


