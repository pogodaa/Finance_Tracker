from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)  # Пароль хранится в виде хеша
    sessions = relationship("Session", back_populates="user")  # Связь с сессиями


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, nullable=False)  # Уникальный идентификатор сессии
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Ссылка на пользователя
    created_at = Column(String(10))  # Дата создания (ДД-ММ-ГГГГ)
    expires_at = Column(Integer)     # Время истечения (timestamp)
    user = relationship("User", back_populates="sessions")  # Связь с пользователем