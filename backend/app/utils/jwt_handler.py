from jose import jwt
from datetime import datetime, timedelta
from app.config.settings import settings


def create_token(data: dict):
    """Crea un JWT con expiración de 24 horas."""
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def decode_token(token: str):
    """Decodifica y valida un JWT. Retorna el payload o None si es inválido."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except Exception:
        return None
