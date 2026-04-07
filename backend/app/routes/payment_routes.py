from fastapi import APIRouter
from app.controllers.payment_controller import create_payment, get_payments

router = APIRouter(prefix="/payments", tags=["Payments"])

router.add_api_route("/", create_payment, methods=["POST"])
router.add_api_route("/", get_payments, methods=["GET"])
