from flask import Blueprint
from app.controller.user_controller import dashboard_user

user_bp = Blueprint("user_bp", __name__)
user_bp.route("/dashboard", methods=["GET"])(dashboard_user)
