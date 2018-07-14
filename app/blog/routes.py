from flask import render_template
from app import db
from app.blog import bp


@bp.route('/<string:page_name>/')
def render_static(page_name):
    return render_template("blog/{}".format(page_name))