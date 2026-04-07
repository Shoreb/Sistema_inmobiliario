from app.config.database import get_connection, get_dict_cursor
from fastapi import HTTPException


def create_pqrs_service(data: dict):
    """Registra una nueva PQRS en la base de datos."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        query = """
        INSERT INTO pqrs (user_id, type, message, status, created_at)
        VALUES (%s, %s, %s, 'pendiente', NOW())
        RETURNING id, user_id, type, message, status, created_at
        """

        cursor.execute(query, (
            data["user_id"],
            data["type"],
            data["message"]
        ))

        nueva_pqrs = cursor.fetchone()
        conn.commit()

        return {
            "message": "PQRS enviada correctamente",
            "pqrs": dict(nueva_pqrs)
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear PQRS: {str(e)}")

    finally:
        cursor.close()
        conn.close()


def get_pqrs_service():
    """Retorna todas las PQRS registradas."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("SELECT * FROM pqrs ORDER BY created_at DESC")
        pqrs_list = cursor.fetchall()
        return [dict(p) for p in pqrs_list]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener PQRS: {str(e)}")

    finally:
        cursor.close()
        conn.close()
