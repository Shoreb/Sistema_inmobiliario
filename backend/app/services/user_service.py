from app.config.database import get_connection, get_dict_cursor
from fastapi import HTTPException


def get_all_users():
    """Retorna la lista de todos los usuarios (sin contraseña)."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("SELECT id, name, last_name, email, tel, role FROM users ORDER BY id")
        users = cursor.fetchall()
        return [dict(u) for u in users]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

    finally:
        cursor.close()
        conn.close()


def get_user_by_id(user_id: int):
    """Retorna un usuario específico por su ID."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute(
            "SELECT id, name, last_name, email, tel, role FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return dict(user)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

    finally:
        cursor.close()
        conn.close()
