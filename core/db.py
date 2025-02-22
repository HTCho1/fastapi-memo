from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


id = "root"
password = "9027yw08"
DATABASE_URL = f"mysql+aiomysql://{id}:{password}@localhost/my_memo_app"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine,
    class_=AsyncSession)

Base = declarative_base()