from flask import Blueprint, jsonify, request
from app.utils.jwt_utils import token_required, role_required

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/dashboard_admin", methods=["GET"])
@token_required
@role_required("admin")
def dashboard_admin():

    user = request.user  # <-- ambil data dari token

    data = {
        "stats": {
            "totalUsers": 10,
            "totalContent": 8,
            "arUsers": 4
        },
        "monthlyData": [20, 30, 45, 50, 40, 60, 72, 90, 100, 85, 70, 50]
    }

    return jsonify({
        "message": f"Selamat datang admin {user['user_id']}",
        "data": data
    }), 200
