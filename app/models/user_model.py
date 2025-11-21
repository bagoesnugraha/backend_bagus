import pymysql
from werkzeug.security import generate_password_hash

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

def create_user(username, email, password, role):
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username=%s OR email=%s",
                (username, email)
            )
            existing = cursor.fetchone()

            if existing:
                return False, "Username atau email sudah digunakan"

            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_password, role)
            )
            conn.commit()

        return True, "User berhasil didaftarkan"

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()
