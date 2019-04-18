import os
from flask_flatpages.utils import pygmented_markdown
from flask import render_template_string

basedir = os.path.abspath(os.path.dirname(__file__))

def my_renderer(text):
    prerendered_body = render_template_string(text)
    return pygmented_markdown(prerendered_body)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = False 
    POSTS_PER_PAGE = 5
    FLATPAGES_HTML_RENDERER = my_renderer
    FLATPAGES_AUTO_RELOAD = DEBUG
    FLATPAGES_EXTENSION = ".md"
    FLATPAGES_ROOT = "content"
    POST_DIR = "posts"

    user = "postgresql"
    password = "testing123"
    database = "post_db"

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@postgres:5432/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
