import jwt
from flask import request, jsonify
from datetime import datetime, timedelta
from functools import wraps

# SECRET KEY – harus sama dengan auth_controller
SECRET_KEY = "rahasia_banget_bagus"

# ============================
# Generate Token
# ============================
def generate_jwt(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# ============================
# Token Required Middleware
# ============================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Ambil token dari header Authorization
        if "Authorization" in request.headers:
            header = request.headers["Authorization"]
            if header.startswith("Bearer "):
                token = header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token missing!"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = payload  # simpan payload user
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token invalid!"}), 401

        return f(*args, **kwargs)
    return decorated

# ============================
# Role Required Middleware
# ============================
def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = request.user.get("role")

            if user_role.lower() != role_name.lower():
                return jsonify({"error": "Access forbidden!"}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator
