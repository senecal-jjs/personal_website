from flask import Blueprint

bp = Blueprint('image_search', __name__)

from app.image_search import routes