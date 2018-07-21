from flask import render_template
from app import db
from app.blog import bp
from app.models import Post 
from flask import current_app