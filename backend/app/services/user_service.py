from app.config.database import get_connection


def get_all_users():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id,name,last_name,email,tel,role FROM users")

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users


def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id,name,last_name,email,tel,role FROM users WHERE id=%s", (user_id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user