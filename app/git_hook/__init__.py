from flask import Blueprint

bp = Blueprint('git_hook', __name__, url_prefix='')

from app.git_hook import routes 