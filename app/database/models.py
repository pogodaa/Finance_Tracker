from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)  # Пароль хранится в виде хеша
    sessions = relationship("Session", back_populates="user")  # Связь с сессиями
    transactions = relationship("Transaction", back_populates="user")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, nullable=False)  # Уникальный идентификатор сессии
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Ссылка на пользователя
    created_at = Column(String(10))  # Дата создания (ДД-ММ-ГГГГ)
    expires_at = Column(Integer)     # Время истечения (timestamp)
    user = relationship("User", back_populates="sessions")  # Связь с пользователем


class TransactionType(Base):
    __tablename__ = "transaction_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)  # "income" или "expense"
    display_name = Column(String(30), nullable=False)  # "Доход" или "Расход"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # "Еда", "Транспорт", "Зарплата" и т.д.


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {'sqlite_autoincrement': True}  # Для автоинкремента ID

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)  # Сумма (отрицательная для расходов)
    description = Column(String(200), nullable=True)
    created_at = Column(String(10), nullable=False)  # ДД-ММ-ГГГГ
    timestamp = Column(Integer, nullable=False)  # Для сортировки
    
    # Связи
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("transaction_types.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    # Отношения
    user = relationship("User", back_populates="transactions")
    type = relationship("TransactionType")
    category = relationship("Category")


def init_db_data(db: Session):
    """Заполняет базу начальными данными (типы транзакций и категории)"""
    # Проверяем, есть ли уже типы транзакций
    if not db.query(TransactionType).count():
        db.add_all([
            TransactionType(name="income", display_name="Доход"),
            TransactionType(name="expense", display_name="Расход")
        ])
    
    # Проверяем категории
    if not db.query(Category).count():
        db.add_all([
            Category(name="Еда"),
            Category(name="Транспорт"),
            Category(name="Развлечения"),
            Category(name="Здоровье"),
            Category(name="Зарплата"),
            Category(name="Другое")
        ])
    
    db.commit()