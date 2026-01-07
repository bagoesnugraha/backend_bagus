from app.db import get_db_connection

# ==============================
# GET ALL USERS
# ==============================
def get_all_users():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, role FROM users ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


# ==============================
# GET USER BY EMAIL
# ==============================
def get_user_by_email(email):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    data = cursor.fetchone()
    cursor.close()
    db.close()
    return data


# ==============================
# GET USER BY USERNAME / EMAIL
# ==============================
def get_user_by_username_or_email(username_or_email):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE email=%s OR username=%s",
        (username_or_email, username_or_email)
    )
    data = cursor.fetchone()
    cursor.close()
    db.close()
    return data


# ==============================
# CREATE USER (ADMIN)
# ==============================
def create_user(username, email, password, role):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM users WHERE email=%s OR username=%s",
        (email, username)
    )
    if cursor.fetchone():
        cursor.close()
        db.close()
        raise Exception("Username atau email sudah terdaftar")

    cursor.execute(
        """
        INSERT INTO users (username, email, password, role)
        VALUES (%s, %s, %s, %s)
        """,
        (username, email, password, role)
    )

    db.commit()
    cursor.close()
    db.close()
    return True


# ==============================
# GET USER BY ID
# ==============================
def get_user_by_id(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, username, email, role FROM users WHERE id=%s",
        (user_id,)
    )
    data = cursor.fetchone()
    cursor.close()
    db.close()
    return data


# ==============================
# 🔥 UPDATE USER
# ==============================
def update_user(user_id, username=None, email=None, role=None, password=None):
    db = get_db_connection()
    cursor = db.cursor()

    fields = []
    values = []

    if username:
        fields.append("username=%s")
        values.append(username)
    if email:
        fields.append("email=%s")
        values.append(email)
    if role:
        fields.append("role=%s")
        values.append(role)
    if password:
        fields.append("password=%s")
        values.append(password)

    if not fields:
        raise Exception("Tidak ada data yang diubah")

    values.append(user_id)
    sql = f"UPDATE users SET {', '.join(fields)} WHERE id=%s"
    cursor.execute(sql, tuple(values))

    db.commit()
    cursor.close()
    db.close()
    return True
