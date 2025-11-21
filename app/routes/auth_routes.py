from flask import Blueprint, jsonify, request
from app.controller.auth_controller import login
from app.utils.jwt_utils import token_required, role_required   # <- ambil dari utils

auth_bp = Blueprint("auth", __name__)

# ---------------------
# ROUTE LOGIN
# ---------------------
auth_bp.add_url_rule("/login", view_func=login, methods=["POST"])

# ---------------------
# ROUTE USER (ROLE: USER)
# ---------------------
@auth_bp.route("/dashboard", methods=["GET"])
@token_required
@role_required("user")
def user_dashboard():
    user = request.user
    return jsonify({
        "message": f"Selamat datang user {user['user_id']}!"
    })

# ---------------------
# ROUTE ADMIN (ROLE: ADMIN)
# ---------------------
@auth_bp.route("/admin", methods=["GET"])
@token_required
@role_required("admin")
def admin_dashboard():
    user = request.user
    return jsonify({
        "message": f"Selamat datang admin {user['user_id']}!"
    })
