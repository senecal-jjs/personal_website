from flask import Blueprint

bp = Blueprint('git_hook', __name__)

from app.git_hook import routes 