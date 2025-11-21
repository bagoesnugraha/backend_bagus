from flask import request, jsonify
from app.models.user_model import create_user

def register_user():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # ROLE DITAMBAH

    if not username or not email or not password or not role:
        return jsonify({"error": "Semua field harus diisi"}), 400

    success, message = create_user(username, email, password, role)

    if success:
        return jsonify({"message": message}), 201
    else:
        return jsonify({"error": message}), 400
