import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Retorna una conexión a PostgreSQL (Supabase)."""
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn


def get_dict_cursor(conn):
    """Retorna un cursor que devuelve filas como diccionarios."""
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
