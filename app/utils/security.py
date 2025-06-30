from passlib.context import CryptContext
import secrets


# Настраиваем контекст хеширования (используем bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хеширует пароль с помощью bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, совпадает ли пароль с хешем."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_session_id() -> str:
    """Генерирует уникальный session_id."""
    return secrets.token_urlsafe(32)

