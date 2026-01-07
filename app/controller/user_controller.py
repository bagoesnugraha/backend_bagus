from flask import jsonify
from app.utils.jwt_utils import verify_jwt

def dashboard_user():
    return jsonify({"message": "Selamat datang di dashboard pengguna"})
