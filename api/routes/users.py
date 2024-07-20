from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, UserCreate, UserLogin
from core.security import get_db, get_password_hash, verify_password


router = APIRouter()


# 회원 가입
@router.post("/signup")
async def signup(signup_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == signup_data.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 동일한 사용자 이름이 가입되어 있습니다. 다른 이름으로 가입해주세요.")
    hashed_password = get_password_hash(signup_data.password)
    new_user = User(username=signup_data.username, email=signup_data.email, hashed_password=hashed_password)
    db.add(new_user)
    
    try:
        await db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="회원가입에 실패했습니다. 기입한 내용을 확인해보세요.")
    
    await db.refresh(new_user)
    return {"message": "회원가입에 성공했습니다."}


# 로그인
@router.post("/login")
async def login(request: Request, sigin_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == sigin_data.username))
    user = result.scalars().first()
    if user and verify_password(sigin_data.password, user.hashed_password):
        request.session["username"] = user.username
        return {"message": "로그인에 성공했습니다."}
    else:
        raise HTTPException(status_code=401, detail="로그인에 실패했습니다.")


# 로그아웃
@router.post("/logout")
async def logout(request: Request):
    request.session.pop("username", None)
    return {"message": "로그아웃에 성공했습니다."}
