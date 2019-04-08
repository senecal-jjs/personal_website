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
    DEBUG = False 
    POSTS_PER_PAGE = 5
    FLATPAGES_HTML_RENDERER = my_renderer
    FLATPAGES_AUTO_RELOAD = DEBUG
    FLATPAGES_EXTENSION = ".md"
    FLATPAGES_ROOT = "content"
    POST_DIR = "posts"

    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('POSTGRES_HOST')
    database = os.environ.get('POSTGRES_DB')
    port = os.environ.get('POSTGRES_PORT')

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
