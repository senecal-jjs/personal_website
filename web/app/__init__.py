import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from flask_flatpages import FlatPages
from config import Config

bootstrap = Bootstrap()
pages = FlatPages()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
    app.config['REPO_PATH'] = os.environ.get('REPO_PATH')

    bootstrap.init_app(app)
    pages.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    from app.image_search import bp as image_search_bp
    app.register_blueprint(image_search_bp)

    return app

