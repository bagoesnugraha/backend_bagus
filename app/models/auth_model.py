from app.db import get_db_connection

def get_user_for_login(email_or_username):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    sql = """
        SELECT * FROM users 
        WHERE email = %s OR username = %s
        LIMIT 1
    """

    cursor.execute(sql, (email_or_username, email_or_username))
    user = cursor.fetchone()

    cursor.close()
    db.close()
    return user
