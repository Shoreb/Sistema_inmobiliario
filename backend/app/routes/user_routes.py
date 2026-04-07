from fastapi import APIRouter
from app.controllers.user_controller import get_users, get_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def users():
    return get_users()


@router.get("/{user_id}")
def user(user_id: int):
    return get_user(user_id)
