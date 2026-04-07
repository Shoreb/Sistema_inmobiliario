from app.config.database import get_connection, get_dict_cursor
from fastapi import HTTPException


def get_all_lots():
    """Retorna todos los lotes disponibles."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("SELECT * FROM lots ORDER BY id")
        lots = cursor.fetchall()
        return [dict(lot) for lot in lots]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lotes: {str(e)}")

    finally:
        cursor.close()
        conn.close()


def add_lot(lot: dict):
    """Inserta un nuevo lote en la base de datos."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        query = """
        INSERT INTO lots (area, location, price, stage, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, area, location, price, stage, status
        """

        cursor.execute(query, (
            lot["area"],
            lot["location"],
            lot["price"],
            lot["stage"],
            lot["status"]
        ))

        nuevo_lote = cursor.fetchone()
        conn.commit()

        return {
            "message": "Lote creado correctamente",
            "lot": dict(nuevo_lote)
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear lote: {str(e)}")

    finally:
        cursor.close()
        conn.close()


def update_lot_status(lot_id: int, status: str):
    """Actualiza el estado de un lote (disponible / reservado / vendido)."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute(
            "UPDATE lots SET status = %s WHERE id = %s RETURNING id, status",
            (status, lot_id)
        )
        updated = cursor.fetchone()

        if not updated:
            raise HTTPException(status_code=404, detail="Lote no encontrado")

        conn.commit()
        return {"message": "Estado actualizado", "lot": dict(updated)}

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar lote: {str(e)}")

    finally:
        cursor.close()
        conn.close()
