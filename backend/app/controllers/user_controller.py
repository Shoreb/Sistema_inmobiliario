from app.services.user_service import get_all_users, get_user_by_id


def get_users():
    """Retorna todos los usuarios."""
    return get_all_users()


def get_user(user_id: int):
    """Retorna un usuario por ID."""
    return get_user_by_id(user_id)
