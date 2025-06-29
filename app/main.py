from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.routers import auth  # Импортируем роутер

# uvicorn app.main:app --reload

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Подключаем роутер auth.py ПЕРВЫМ (чтобы его роуты имели приоритет)
app.include_router(auth.router)

# Остальные роуты (главная, about и т. д.)
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
async def home(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/auth/login")
async def home(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})