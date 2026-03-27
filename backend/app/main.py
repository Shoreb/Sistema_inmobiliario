from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import get_connection

from app.routes import (
    auth_routes,
    user_routes,
    lot_routes,
    payment_routes,
    pqrs_routes
)

app = FastAPI(title="Sistema Inmobiliario API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(lot_routes.router)
app.include_router(payment_routes.router)
app.include_router(pqrs_routes.router)

@app.get("/")
def root():
    return {"message": "API Sistema Inmobiliario funcionando"}

@app.get("/test-db")
def test_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE();")
    db = cursor.fetchone()

    cursor.close()
    conn.close()

    return {"database": db}

from flask import Flask, request, jsonify
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexión a MySQL
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# REGISTRO
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    # Encriptar contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()
        return jsonify({"message": "Usuario registrado"})
    except:
        return jsonify({"error": "Email ya existe"})
    finally:
        cursor.close()
        conn.close()

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, password FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        user_id, name, hashed_password = user

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return jsonify({
                "message": "Login exitoso",
                "user": {
                    "id": user_id,
                    "name": name
                }
            })
    
    return jsonify({"error": "Credenciales incorrectas"}), 401


if __name__ == '__main__':
    app.run(debug=True)