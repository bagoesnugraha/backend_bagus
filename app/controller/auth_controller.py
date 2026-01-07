from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user_model import get_user_by_username_or_email, create_user
from app.utils.jwt_utils import generate_jwt

# ============================
# REGISTER
# ============================
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password_raw = data.get("password")
    role = data.get("role", "user")

    password_hashed = generate_password_hash(password_raw)
    create_user(username, email, password_hashed, role)

    return jsonify({
        "success": True,
        "message": "User berhasil dibuat"
    })


# ============================
# LOGIN (MOBILE & WEB)
# ============================
def login():
    data = request.get_json()

    username_or_email = data.get("username_or_email")
    password = data.get("password")

    user = get_user_by_username_or_email(username_or_email)

    if not user:
        return jsonify({"success": False, "message": "User tidak ditemukan"}), 400

    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Password salah"}), 400

    token = generate_jwt(user["id"], user["role"])

    return jsonify({
        "success": True,
        "message": "Login berhasil",
        "token": token,
        "role": user["role"]
    })
