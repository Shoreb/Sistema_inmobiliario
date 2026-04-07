from fastapi import HTTPException
from app.models.user_model import UserCreate, UserLogin
from app.services.auth_service import authenticate_user, create_user


async def register(user: UserCreate):
    """Endpoint de registro — valida datos con Pydantic antes de procesarlos."""
    return create_user(user.model_dump())


async def login(data: UserLogin):
    """Endpoint de login — retorna JWT si las credenciales son correctas."""
    result = authenticate_user(data.email, data.password)

    if not result:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return result
