from flask import Blueprint

bp = Blueprint('riotgames', __name__)

from app.riotgames import routes
