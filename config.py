import os
from dotenv import load_dotenv
from flask_flatpages.utils import pygmented_markdown
from flask import render_template_string

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def my_renderer(text):
    prerendered_body = render_template_string(text)
    return pygmented_markdown(prerendered_body)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    DEBUG = True
    POSTS_PER_PAGE = 5
    FLATPAGES_HTML_RENDERER = my_renderer
    FLATPAGES_AUTO_RELOAD = DEBUG
    FLATPAGES_EXTENSION = ".md"
    FLATPAGES_ROOT = "content"
    POST_DIR = "posts"
