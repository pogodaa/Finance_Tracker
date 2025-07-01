from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from ..database.database import get_db
from ..database.models import Transaction, Category, TransactionType
from ..database.crud import TransactionCRUD
from ..utils.auth import get_current_user
from ..utils.export_utils import export_to_csv, export_to_excel
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["transactions"])
templates = Jinja2Templates(directory="app/templates")

@router.post("/add")
async def add_transaction(
    request: Request,
    amount: int = Form(...),
    type: str = Form(...),
    category: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    # Проверка максимальной суммы
    if amount > 10000000:
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "user": user,
                "error": "Максимальная сумма - 10 000 000 ₽",
                "categories": db.query(Category).all(),
                "transactions": TransactionCRUD.get_user_transactions(db, user.id),
                "total_income": ...,
                "total_expense": ...,
                "category_percents": ...
            },
            status_code=400
        )
    
    # Проверка длины описания
    if description and len(description) > 50:
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "user": user,
                "error": "Описание не должно превышать 50 символов",
                "categories": db.query(Category).all(),
                "transactions": TransactionCRUD.get_user_transactions(db, user.id),
                "total_income": ...,
                "total_expense": ...,
                "category_percents": ...
            },
            status_code=400
        )
    
    TransactionCRUD.create_transaction(
        db=db,
        user_id=user.id,
        amount=amount,
        type_name=type,
        category_name=category,
        description=description
    )
    
    return RedirectResponse(url="/home", status_code=303)

@router.get("", response_class=HTMLResponse)
async def view_all_transactions(
    request: Request,
    db: Session = Depends(get_db)
):
    # Проверяем авторизацию
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    # Получаем ВСЕ транзакции пользователя (с сортировкой по дате)
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user.id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )
    
    # Получаем статистику
    stats = TransactionCRUD.get_monthly_stats(db, user.id)
    
    return templates.TemplateResponse(
        "transactions.html",  # Создадим этот шаблон
        {
            "request": request,
            "user": user,
            "transactions": transactions,
            "total_income": stats['income'],
            "total_expense": stats['expenses'],
            "category_percents": stats['category_percents']
        }
    )

@router.post("/delete/{transaction_id}")
async def delete_transaction(
    request: Request,
    transaction_id: int,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    if TransactionCRUD.delete_transaction(db, transaction_id, user.id):
        return RedirectResponse(url="/transactions", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Transaction not found")
    

@router.get("/export/{export_type}")
async def export_transactions(
    request: Request,
    export_type: str,  # csv или excel
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user.id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )
    
    if export_type == 'csv':
        file = export_to_csv(transactions)
        media_type = "text/csv"
        filename = f"transactions_{datetime.now().strftime('%Y-%m-%d')}.csv"
    elif export_type == 'excel':
        file = export_to_excel(transactions)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"transactions_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    else:
        raise HTTPException(status_code=400, detail="Invalid export type")
    
    return StreamingResponse(
        file,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )