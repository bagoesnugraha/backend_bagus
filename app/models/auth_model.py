import pymysql
from werkzeug.security import check_password_hash

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

def login_user(username_or_email, password):
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:

            # Bisa login pakai username atau email
            cursor.execute(
                "SELECT * FROM users WHERE username=%s OR email=%s",
                (username_or_email, username_or_email)
            )
            user = cursor.fetchone()

            if not user:
                return False, "User tidak ditemukan"

            # Cek password hash
            if not check_password_hash(user["password"], password):
                return False, "Password salah"

            # 🔥 NORMALISASI ROLE (WAJIB)
            user["role"] = user["role"].lower()

            return True, user

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()
