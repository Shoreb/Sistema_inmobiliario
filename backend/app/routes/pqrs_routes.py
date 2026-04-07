from fastapi import APIRouter
from app.controllers.pqrs_controller import create_pqrs, get_pqrs

router = APIRouter(prefix="/pqrs", tags=["PQRS"])

router.add_api_route("/", create_pqrs, methods=["POST"])
router.add_api_route("/", get_pqrs, methods=["GET"])
