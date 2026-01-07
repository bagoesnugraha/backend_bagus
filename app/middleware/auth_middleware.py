from flask import request, jsonify
from app.utils.jwt_utils import verify_jwt

def admin_required():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None, jsonify({
            "success": False,
            "message": "Token tidak ditemukan"
        }), 401

    token = auth_header.replace("Bearer ", "")

    decoded = verify_jwt(token)
    if not decoded or decoded.get("error"):
        return None, jsonify({
            "success": False,
            "message": "Token tidak valid"
        }), 401

    if decoded.get("role") != "admin":
        return None, jsonify({
            "success": False,
            "message": "Akses ditolak! Khusus admin"
        }), 403

    return decoded, None, None
