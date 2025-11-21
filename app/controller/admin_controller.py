from flask import Blueprint, jsonify, request
import pymysql
import jwt

SECRET_KEY = "agriminds_secret_key"  # samakan dengan di login

admin_bp = Blueprint("admin", __name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "project_baru"
}

def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )


# ============================================
# 🔐 Middleware: cek token & role = admin
# ============================================
def require_admin(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return jsonify({"error": "Token tidak ada, login dulu"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if decoded.get("role") != "admin":
                return jsonify({"error": "Akses ditolak, hanya admin"}), 403

        except Exception as e:
            return jsonify({"error": f"Token invalid: {str(e)}"}), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper



# ============================================
# 📌 GET /admin/dashboard
# ============================================
@admin_bp.route("/admin/dashboard", methods=["GET"])
@require_admin
def dashboard_admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Total user
        cursor.execute("SELECT COUNT(*) AS total FROM users")
        total_users = cursor.fetchone()["total"]

        # Total konten
        cursor.execute("SELECT COUNT(*) AS total FROM konten")
        total_konten = cursor.fetchone()["total"]

        # Pengguna AR
        cursor.execute("SELECT COUNT(*) AS total FROM users WHERE role='ar'")
        ar_users = cursor.fetchone()["total"]

        # Grafik dummy dulu
        monthly_data = [
            {"month": "Jan", "users": 15, "content": 8},
            {"month": "Feb", "users": 25, "content": 12},
            {"month": "Mar", "users": 40, "content": 20},
        ]

        return jsonify({
            "stats": {
                "totalUsers": total_users,
                "totalContent": total_konten,
                "arUsers": ar_users
            },
            "monthlyData": monthly_data
        })

    finally:
        conn.close()
