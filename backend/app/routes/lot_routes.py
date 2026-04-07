from fastapi import APIRouter
from app.controllers.lot_controller import get_lots, create_lot

router = APIRouter(prefix="/lots", tags=["Lots"])

router.add_api_route("/", get_lots, methods=["GET"])
router.add_api_route("/", create_lot, methods=["POST"])
