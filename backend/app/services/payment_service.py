from app.config.database import get_connection, get_dict_cursor
from fastapi import HTTPException


def create_payment_service(payment: dict):
    """Registra un pago en la base de datos."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        # Verificar que la compra existe
        cursor.execute("SELECT id FROM purchases WHERE id = %s", (payment["purchase_id"],))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="La compra no existe")

        query = """
        INSERT INTO payments (purchase_id, amount, payment_date)
        VALUES (%s, %s, NOW())
        RETURNING id, purchase_id, amount, payment_date
        """

        cursor.execute(query, (
            payment["purchase_id"],
            payment["amount"]
        ))

        nuevo_pago = cursor.fetchone()
        conn.commit()

        return {
            "message": "Pago registrado correctamente",
            "payment": dict(nuevo_pago)
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar pago: {str(e)}")

    finally:
        cursor.close()
        conn.close()


def get_payments_service():
    """Retorna todos los pagos registrados."""

    conn = get_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("SELECT * FROM payments ORDER BY payment_date DESC")
        payments = cursor.fetchall()
        return [dict(p) for p in payments]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pagos: {str(e)}")

    finally:
        cursor.close()
        conn.close()
