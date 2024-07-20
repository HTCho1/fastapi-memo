from fastapi import APIRouter
from api.routes import users, memos


api_router = APIRouter()
api_router.include_router(users.router, tags=["users"])
api_router.include_router(memos.router, tags=["memos"])