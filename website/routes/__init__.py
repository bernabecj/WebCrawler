from flask import Blueprint

routes = Blueprint("routes", __name__)

from . import register_routes_views
