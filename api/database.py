import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL='postgresql+asyncpg://postgres.wqvtwctdjevzldwpderu:0123456789Ziad@aws-1-eu-north-1.pooler.supabase.com:6543/postgres'

print("DATABASE_URL:", DATABASE_URL) 
# إعداد SSL
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"ssl": ssl_context}  
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
