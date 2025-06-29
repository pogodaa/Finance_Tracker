from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # Импортируем Base из models.py

# Подключение к SQLite (файл БД будет создан в корне проекта как `finance.db`)
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.db"

# Создаем "движок" SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Нужно только для SQLite
)

# Создаем фабрику сессий (каждое обращение к БД — новая сессия)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы в БД (если их нет)
Base.metadata.create_all(bind=engine)

# Функция для получения сессии БД (будет использоваться в зависимостях FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()