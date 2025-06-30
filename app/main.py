from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.routers import auth  # Импортируем роутер
from fastapi.responses import RedirectResponse

from fastapi import Depends
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user
from app.database.database import get_db

# uvicorn app.main:app --reload

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Подключаем роутер auth.py ПЕРВЫМ (чтобы его роуты имели приоритет)
app.include_router(auth.router)


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
    
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "user": user}
    )