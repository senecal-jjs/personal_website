from flask import render_template
from app import db
from app.blog import bp
from app.models import Post 
from flask import current_app
from app import pages 
from flask_flatpages import pygments_style_defs

@bp.route('/blog/<string:page_name>/')
def render_static(page_name):
    post_dir = current_app.config['POST_DIR']
    path = "{}/{}".format(post_dir, page_name)
    post = pages.get_or_404(path)
    return render_template("page.html", post=post)

@bp.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}