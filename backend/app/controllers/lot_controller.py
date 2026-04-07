from app.models.lot_model import LotCreate
from app.services.lot_service import get_all_lots, add_lot


async def get_lots():
    """Retorna todos los lotes."""
    return get_all_lots()


async def create_lot(lot: LotCreate):
    """Crea un nuevo lote."""
    return add_lot(lot.model_dump())
