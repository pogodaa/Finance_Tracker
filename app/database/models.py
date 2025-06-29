from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)  # bcrypt


# class Category(Base):
#     __tablename__ = "categories"
#     __table_args__ = (
#         UniqueConstraint('name', 'user_id', name='unique_category_per_user'),
#     )

#     id = Column(Integer, primary_key=True)
#     name = Column(String(20), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
#     is_default = Column(Boolean, default=False)
#     order = Column(Integer, default=0)


# class TransactionType(str, enum.Enum):
#     INCOME = "income"
#     EXPENSE = "expense"

# class Transaction(Base):
#     __tablename__ = "transactions"

#     id = Column(Integer, primary_key=True, index=True)
#     amount = Column(Numeric(10, 0), nullable=False)
#     description = Column(String(200), nullable=True)
#     date = Column(Date, default=date.today, nullable=False)
#     type_deal = Column(Enum(TransactionType), nullable=False)  # Чистый Enum
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)