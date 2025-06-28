from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# uvicorn app.main:app --reload

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
async def home(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/login")
async def home(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.get("/register")
async def home(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})