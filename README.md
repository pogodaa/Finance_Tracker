# Finance Tracker - Персональный финансовый менеджер

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)

Система для учёта личных финансов с аналитикой и экспортом данных.

## 📌 Основной функционал

### 💰 Управление транзакциями
- Добавление доходов/расходов
- Просмотр истории операций
- Удаление транзакций
- Категоризация (еда, транспорт, зарплата и др.)

### 📊 Аналитика
- Общий баланс (доходы - расходы)
- Статистика
- Распределение расходов по категориям (%)
- Последние 4 операции на главной

### 🔐 Безопасность
- Регистрация с валидацией паролей:
  - Минимум 8 символов
  - Обязательные цифры и спецсимволы
- Защищённые сессии с куками
- Хеширование паролей (bcrypt)

### 📁 Экспорт данных
- Скачивание в CSV
- Скачивание в Excel (XLSX)
- Автоформатирование файлов

## 🛠 Технологический стек
- **Backend**: Python + FastAPI
- **Frontend**: Jinja2 + HTML/CSS (без JavaScript)
- **База данных**: SQLite + SQLAlchemy ORM
- **Аутентификация**: Сессии + куки

## 🚀 Запуск проекта
- python run.py
- uvicorn app.main:app --reload

### Требования
- Python 3.8+
- Установленные зависимости из `requirements.txt`