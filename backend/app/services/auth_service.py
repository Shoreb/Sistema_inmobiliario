from app.config.database import get_connection
from app.utils.password import hash_password, verify_password
from app.utils.jwt_handler import create_token


def create_user(user: dict):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    password_hash = hash_password(user["password"])

    query = """
    INSERT INTO users (name, last_name, email, tel, password)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user["name"],
        user["last_name"],
        user["email"],
        user["tel"],
        password_hash
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Usuario creado correctamente"}


def authenticate_user(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    token = create_token({
        "id": user["id"],
        "email": user["email"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }