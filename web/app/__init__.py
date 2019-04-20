import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_flatpages import FlatPages
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
pages = FlatPages()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
    app.config['REPO_PATH'] = os.environ.get('REPO_PATH')

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    pages.init_app(app)

    # with app.app_context():
    #     db.create_all()

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    from app.image_search import bp as image_search_bp
    app.register_blueprint(image_search_bp)

    from app.git_hook import bp as git_hook_bp
    app.register_blueprint(git_hook_bp)

    return app

from app import models
