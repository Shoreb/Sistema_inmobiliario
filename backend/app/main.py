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