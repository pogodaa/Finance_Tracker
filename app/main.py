from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.database.crud import TransactionCRUD
from app.database.models import Category, Transaction
from app.utils.auth import get_current_user
from app.routers import auth, transactions


# uvicorn app.main:app --reload

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# Подключаем роутер auth.py ПЕРВЫМ (чтобы его роуты имели приоритет)
app.include_router(auth.router)
app.include_router(transactions.router)  


# Остальные роуты (главная, about и т. д.)
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user}
    )


@app.get("/about")
async def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return templates.TemplateResponse(
        "about.html",
        {"request": request, "user": user}
    )


@app.get("/home")
async def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    # Берем только 4 последние транзакции
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user.id)
        .order_by(Transaction.timestamp.desc())
        .limit(4)  # <-- Вот это ограничение
        .all()
    )
    
    stats = TransactionCRUD.get_monthly_stats(db, user.id)
    
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "user": user,
            "transactions": transactions,
            "total_income": stats['income'],
            "total_expense": stats['expenses'],
            "category_percents": stats['category_percents'],
            "categories": db.query(Category).all()
        }
    )