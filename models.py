from pydantic import BaseModel
from typing import Optional
from core.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(200))
    hashed_password = Column(String(512))
    
    
class Memo(Base):
    __tablename__ = "memo"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(100))
    content = Column(String(1000))


# 회원가입시 데이터 검증
class UserCreate(BaseModel):
    username: str
    email: str
    password: str # 해시전 패스워드를 받습니다.
    
    
# 회원로그인시 데이터 검증
class UserLogin(BaseModel):
    username: str
    password: str # 해시전 패스워드를 받습니다.


class MemoCreate(BaseModel):
    title: str
    content: str
    
    
class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    