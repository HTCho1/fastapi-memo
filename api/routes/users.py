from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, UserCreate, UserLogin
from core.security import get_db, get_password_hash, verify_password


router = APIRouter()


# 회원 가입
@router.post("/signup")
async def signup(signup_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # async
    result = await db.execute(select(User).where(User.username == signup_data.username))  # where를 filter로 써도됨
    # 먼저 username이 이미 존재하는지 확인
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 동일 사용자 이름이 가입되어 있습니다.")
    hashed_password = get_password_hash(signup_data.password)
    new_user = User(username=signup_data.username, email=signup_data.email, hashed_password=hashed_password)
    db.add(new_user)
    
    try:
        await db.commit()
    except Exception as e:
        print (e)
        raise HTTPException(status_code=500, detail="회원가입이 실패했습니다. 기입한 내용을 확인해보세요.")
    
    # async
    await db.refresh(new_user)
    return {"message": "회원가입이 성공했습니다."}


# 로그인
@router.post("/login")
async def login(request: Request, signin_data: UserLogin, db: AsyncSession = Depends(get_db)):
    # async
    result = await db.execute(select(User).where(User.username == signin_data.username))
    user = result.scalars().first()
    if user and verify_password(signin_data.password, user.hashed_password):
        request.session["username"] = user.username
        return {"message":"로그인이 성공했습니다."}
    else:
        raise HTTPException(status_code=401, detail="로그인이 실패했습니다.")
    