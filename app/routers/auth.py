from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..database.models import User
from ..utils.security import hash_password
from ..utils.security import verify_password
from ..utils.security import generate_session_id
from fastapi.templating import Jinja2Templates
from fastapi import Response
from fastapi.responses import RedirectResponse
from ..utils import (
    security,
    date_utils,
    auth as auth_utils
)
from ..database.models import Session as SessionModel
import re 

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


def is_valid_password(password):
    if len(password) < 8 or len(password) > 32:
        return "Длина пароля должна быть в диапазоне от 8 до 32 символов!"
        
    if not re.search(r'[A-Z]', password):
        return "Пароль должен содержать хотя бы одну заглавную букву!"
    
    if not re.search(r'[0-9]', password):
        return "Пароль должен содержать хотя бы одну цифру!"
        
    if not re.search(r'[\W_]', password):
        return "Пароль должен содержать хотя бы один специальный символ!"
        
    return None  # Если пароль валиден

# Добавляем GET-обработчик для страницы РЕГИСТРАЦИЯ
@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

# ВХОД
@router.get("/login", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

# ВЫХОД
@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session_id")
    return response


# POST ДЛЯ ВХОДА
@router.post("/login")
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Проверяем пользователя
    user = db.query(User).filter(User.username == username).first()
    if not user or not security.verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Неверный логин или пароль!"}
        )
    
    # Создаём сессию
    session_id = security.generate_session_id()
    date_str, current_timestamp = date_utils.get_current_date()
    expires_at = current_timestamp + 86400  # +24 часа
    
    db_session = SessionModel(
        session_id=session_id,
        user_id=user.id,
        created_at=date_str,
        expires_at=expires_at
    )
    db.add(db_session)
    db.commit()
    
    # Устанавливаем куки
    response = RedirectResponse(url="/home", status_code=303)
    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=86400,
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return response


@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)):
    error = None
    
    # Проверяем пароли
    if password != confirm_password:
        error = "Пароли не совпадают!"
    
    # Проверяем существование пользователя
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        error = "Пользователь с таким именем уже существует!"

    # Проверяем валидность пароля (только если нет других ошибок)
    if not error:
        password_error = is_valid_password(password)
        if password_error:
            error = password_error

    # Если есть ошибка - показываем форму снова
    if error:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": error}
        )

    # Если ошибок нет - создаем пользователя
    new_user = User(
        username=username,
        password_hash=hash_password(password)
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/home", status_code=303)

