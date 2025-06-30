from datetime import datetime

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