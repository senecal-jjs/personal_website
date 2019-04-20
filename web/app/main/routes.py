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
    posts = [ p for p in pages if p.path.startswith(current_app.config['POST_DIR']) ]
    posts.sort(key=lambda item:date_to_int(item['date']), reverse=True)
    return render_template('index.html', posts=posts)

@bp.route('/resume')
def resume():
    return render_template('resume.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/add', methods=['POST'])
def add():
    data = request.get_json(force=True)
    title = data['title']
    body = data['body']
    link = data['link']

    p = Post(title=title, body=body, link=link)
    db.session.add(p)
    db.session.commit()
    return json.dumps("Added"), 200






    


