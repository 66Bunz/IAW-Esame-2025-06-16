from flask import Blueprint

performances_bp = Blueprint('performances', __name__, url_prefix='/performances')

from blueprints.performances import routes