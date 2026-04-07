from fastapi import APIRouter
from app.controllers.auth_controller import login, register

router = APIRouter(prefix="/auth", tags=["Auth"])

router.add_api_route("/register", register, methods=["POST"])
router.add_api_route("/login", login, methods=["POST"])
