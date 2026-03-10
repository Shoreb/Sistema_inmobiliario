from app.config.database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE();")
    db = cursor.fetchone()

    print("Conectado a la base de datos:", db)

    cursor.close()
    conn.close()

except Exception as e:
    print("Error conectando a la base:", e)