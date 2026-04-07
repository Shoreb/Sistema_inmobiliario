from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    auth_routes,
    user_routes,
    lot_routes,
    payment_routes,
    pqrs_routes
)

app = FastAPI(title="Sistema Inmobiliario API")

# Lista de orígenes permitidos
origins = [
    "https://sistemainmobiliario.vercel.app",  # frontend en producción
    "http://localhost:3000",                    # desarrollo local
    "http://localhost:5500",                    # Live Server de VS Code
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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