from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def parse_date(date_str: str) -> tuple[str, int]:
    """Преобразует строку ДД-ММ-ГГГГ в (дату, timestamp)."""
    try:
        day, month, year = map(int, date_str.split('-'))
        dt = datetime(year, month, day)
        return date_str, int(dt.timestamp())
    except:
        return None, None

def format_date(date_str: str) -> str:
    """Форматирует дату для вывода."""
    return date_str if date_str else "не указана"

def get_current_date() -> tuple[str, int]:
    """Возвращает текущую дату в формате (ДД-ММ-ГГГГ, timestamp)."""
    now = datetime.now()
    date_str = f"{now.day:02d}-{now.month:02d}-{now.year}"
    return date_str, int(now.timestamp())



def generate_stats_plot(transactions):
    # Группируем данные по категориям
    categories = {}
    for t in transactions:
        if t.amount < 0:  # Только расходы
            cat = t.category.name
            categories[cat] = categories.get(cat, 0) + abs(t.amount)
    
    if not categories:
        return None
    
    # Создаем график
    plt.figure(figsize=(8, 5))
    plt.pie(
        categories.values(),
        labels=categories.keys(),
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Pastel1.colors
    )
    plt.title('Распределение расходов по категориям')
    
    # Конвертируем в base64 для HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')