from app.models.pqrs_model import PQRSCreate
from app.services.pqrs_service import create_pqrs_service, get_pqrs_service


async def create_pqrs(data: PQRSCreate):
    """Registra una nueva PQRS."""
    return create_pqrs_service(data.model_dump())


async def get_pqrs():
    """Retorna todas las PQRS."""
    return get_pqrs_service()
