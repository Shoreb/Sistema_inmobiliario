import bcrypt


def hash_password(password: str) -> str:
    """Hashea una contraseña con bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Verifica que una contraseña coincida con su hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())
