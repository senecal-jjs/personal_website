from flask import render_template
from app import db
from app.blog import bp
from app.models import Post 
from flask import current_app
from app import pages 


# @bp.route('/blog/<string:page_name>/')
# def render_static(page_name):
#     current_app.config['POSTS_PER_PAGE']
#     p = db.session.query(Post).filter(Post.link == page_name)
#     entry = p[0]
#     return render_template("blog/{}".format(page_name), title=entry.title, date=entry.timestamp)

@bp.route('/blog/<string:page_name>/')
def render_static(page_name):
    post_dir = current_app.config['POST_DIR']
    path = "{}/{}".format(post_dir, page_name)
    post = pages.get_or_404(path)
    return render_template("page.html", post=post)