from datetime import datetime 
import time 
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import pages 
from app.main import bp 

def date_to_int(date):
    date = time.mktime(date.timetuple())
    return date  

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/blog')
def blog():
    posts = [ p for p in pages if p.path.startswith(current_app.config['POST_DIR']) ]
    posts.sort(key=lambda item:date_to_int(item['date']), reverse=True)
    return render_template('blog.html', posts=posts)

@bp.route('/resume')
def resume():
    return render_template('resume.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/projects')
def projects():
    return render_template('projects.html')






    


