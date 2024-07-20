from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, Memo, MemoCreate, MemoUpdate
from core.security import get_db


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 메모 생성
@router.post("/memos/")
async def create_memo(request: Request, memo: MemoCreate, db: AsyncSession = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="승인되지 않은 사용자입니다.")
    # async
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    new_memo = Memo(user_id=user.id, title=memo.title, content=memo.content)
    db.add(new_memo)
    # async
    await db.commit()
    await db.refresh(new_memo)
    return new_memo


# 메모 조회
@router.get("/memos/")
async def list_memos(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="승인되지 않은 사용자입니다.")
    # async
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")    
    
    # async
    result = await db.execute(select(Memo).where(Memo.user_id == user.id))
    memos = result.scalars().all()
    return templates.TemplateResponse("memos.html", {"request": request, "memos": memos, "username": username})


# 메모 수정
@router.put("/memos/{memo_id}")
async def update_memo(request: Request, memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="승인되지 않은 사용자입니다.")
    # async
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")    
    # async 
    result = await db.execute(select(Memo).filter(Memo.user_id == user.id, Memo.id == memo_id))
    db_memo = result.scalars().first()
    if db_memo is None:
        return ({"error": "메모를 찾을 수 없습니다."})

    if memo.title is not None:
        db_memo.title = memo.title
    if memo.content is not None:
        db_memo.content = memo.content
    
    # async
    await db.commit()
    await db.refresh(db_memo)
    return db_memo


# 메모 삭제
@router.delete("/memos/{memo_id}")
async def delete_memo(request: Request, memo_id: int, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="승인되지 않은 사용자입니다.")
    # async
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")     
    
    # async
    result = await db.execute(select(Memo).filter(Memo.user_id == user.id, Memo.id == memo_id))
    db_memo = result.scalars().first()    
    if db_memo is None:
        return ({"error": "메모를 찾을 수 없습니다."})
    
    # async
    await db.delete(db_memo)
    await db.commit()
    return ({"message": "메모를 삭제했습니다."})
