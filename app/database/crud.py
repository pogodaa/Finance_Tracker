from sqlalchemy.orm import Session
from .models import Transaction, TransactionType, Category
from ..utils.date_utils import get_current_date
from typing import List
from sqlalchemy import func  # Импорт для агрегатных функций SQL

class TransactionCRUD:
    @staticmethod
    def create_transaction(
        db: Session,
        user_id: int,
        amount: int,
        type_name: str,  # "income" или "expense"
        category_name: str,
        description: str = None
    ) -> Transaction:
        
        MAX_AMOUNT = 10000000
        MAX_DESCRIPTION_LENGTH = 50
    
        if abs(amount) > MAX_AMOUNT:
            raise ValueError(f"Сумма превышает максимально допустимую ({MAX_AMOUNT} ₽)")
        
        if description and len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Описание не должно превышать {MAX_DESCRIPTION_LENGTH} символов")
        
       # Для расходов делаем отрицательное значение
        if type_name == "expense":
         amount = -abs(amount)
        """Создает новую транзакцию"""
        # Получаем текущую дату
        date_str, timestamp = get_current_date()
        
        # Находим тип транзакции
        transaction_type = db.query(TransactionType).filter(
            TransactionType.name == type_name
        ).first()
        
        # Находим категорию
        category = db.query(Category).filter(
            Category.name == category_name
        ).first()
        
        # Создаем транзакцию
        transaction = Transaction(
            amount=amount,
            description=description,
            created_at=date_str,
            timestamp=timestamp,
            user_id=user_id,
            type_id=transaction_type.id,
            category_id=category.id
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_user_transactions(
        db: Session,
        user_id: int,
        limit: int = 10
    ) -> List[Transaction]:
        """Получает последние транзакции пользователя"""
        return (
            db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.timestamp.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
        """Удаляет транзакцию пользователя"""
        transaction = (
            db.query(Transaction)
            .filter(
                Transaction.id == transaction_id,
                Transaction.user_id == user_id
            )
            .first()
        )
        
        if transaction:
            db.delete(transaction)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_monthly_stats(db: Session, user_id: int):
      """Получает статистику за текущий месяц"""
      from datetime import datetime
      
      # Получаем текущий месяц и год
      now = datetime.now()
      current_month = now.month
      current_year = now.year
      
      # Запросы для доходов и расходов
      income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.amount > 0,
            func.substr(Transaction.created_at, 4, 2) == f"{current_month:02d}",
            func.substr(Transaction.created_at, 7, 4) == str(current_year)
      ).scalar() or 0

      expenses = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.amount < 0,
            func.substr(Transaction.created_at, 4, 2) == f"{current_month:02d}",
            func.substr(Transaction.created_at, 7, 4) == str(current_year)
      ).scalar() or 0

      # Процентное соотношение категорий расходов
      expense_categories = db.query(
            Category.name,
            func.sum(Transaction.amount).label('total')
      ).join(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.amount < 0,
            func.substr(Transaction.created_at, 4, 2) == f"{current_month:02d}",
            func.substr(Transaction.created_at, 7, 4) == str(current_year)
      ).group_by(Category.name).all()

      # Рассчитываем проценты
      category_percents = {}
      total_expenses = abs(expenses)
      
      if total_expenses > 0:
            for cat in expense_categories:
                  percent = round((abs(cat.total) / total_expenses) * 100)
                  category_percents[cat.name] = percent

      return {
            'income': income,
            'expenses': abs(expenses),
            'category_percents': category_percents
      }