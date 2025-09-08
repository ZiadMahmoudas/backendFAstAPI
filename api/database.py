import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ناخد من Environment Variable، ولو مش موجود نستخدم الـ default (للتجربة فقط)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres.wqvtwctdjevzldwpderu:0123456789Ziad"
    "@aws-1-eu-north-1.pooler.supabase.com:6543/postgres?sslmode=require"
)


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dependency للـ DB
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
