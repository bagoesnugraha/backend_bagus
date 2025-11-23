from flask import request, jsonify
from app.models.auth_model import login_user
from app.utils.jwt_utils import generate_jwt

def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body tidak boleh kosong"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username dan password wajib diisi"
        }), 400

    success, result = login_user(username, password)

    if not success:
        return jsonify({
            "success": False,
            "message": result
        }), 401

    role_normalized = result["role"].lower()
    token = generate_jwt(result["id"], role_normalized)

    return jsonify({
        "success": True,
        "message": "Login berhasil",
        "data": {
            "user": {
                "id": result["id"],
                "username": result["username"],
                "role": role_normalized
            },
            "token": token
        }
    }), 200
