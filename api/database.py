from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager

# لو SQLite للتجارب
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:0123456789Ziad@aws-1-eu-north-1.pooler.supabase.com:6543/postgres?sslmode=require"

# انشاء الـ async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Base للـ models
Base = declarative_base()

# Context manager لكل request
@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# دالة init models لو حبيت تعمل create_all
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
