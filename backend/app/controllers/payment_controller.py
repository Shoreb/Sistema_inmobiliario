from app.models.payment_model import PaymentCreate
from app.services.payment_service import create_payment_service, get_payments_service


async def create_payment(payment: PaymentCreate):
    """Registra un pago."""
    return create_payment_service(payment.model_dump())


async def get_payments():
    """Retorna todos los pagos."""
    return get_payments_service()
