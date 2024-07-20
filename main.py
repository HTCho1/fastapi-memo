from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from core.db import Base, engine
from api.main import api_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행될 로직
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 애플리케이션 종료 시 실행될 로직 (필요한 경우)


# 유저가 접근하지 못하도록 Swagger UI와 Redoc 비활성화
app = FastAPI(lifespan=app_lifespan, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.include_router(api_router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
