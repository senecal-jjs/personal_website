from flask import Blueprint

bp = Blueprint('image_search', __name__)

from app.image_search import routes
from app.image_search import helpers 
from app.image_search import settings 
