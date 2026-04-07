from app.config.database import get_connection, get_dict_cursor
from app.utils.password import hash_password, verify_password
from app.utils.jwt_handler import create_token
from fastapi import HTTPException


def create_user(user: dict):
    """Registra un nuevo usuario en la base de datos."""

    # Validar que las contraseñas coincidan
    if user["password"] != user["confirm_password"]:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        # Verificar si el email ya existe
        cursor.execute("SELECT id FROM users WHERE email = %s", (user["email"],))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        password_hash = hash_password(user["password"])

        query = """
        INSERT INTO users (name, last_name, email, tel, password)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, name, email, role
        """

        cursor.execute(query, (
            user["name"],
            user["last_name"],
            user["email"],
            user["tel"],
            password_hash
        ))

        nuevo_usuario = cursor.fetchone()
        conn.commit()

        return {
            "message": "Usuario creado correctamente",
            "user": dict(nuevo_usuario)
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    finally:
        cursor.close()
        conn.close()


def authenticate_user(email: str, password: str):
    """Verifica credenciales y retorna token JWT si son correctas."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

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
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }

    finally:
        cursor.close()
        conn.close()
