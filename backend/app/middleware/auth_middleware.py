from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt_handler import decode_token

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Dependencia de FastAPI para proteger rutas.
    Uso: agregar `current_user: dict = Depends(get_current_user)` en cualquier endpoint.
    """
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    return payload


def require_admin(current_user: dict = Security(get_current_user)):
    """
    Dependencia para rutas que solo puede usar un administrador.
    Uso: `current_user: dict = Depends(require_admin)`
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado — se requiere rol de administrador"
        )
    return current_user
