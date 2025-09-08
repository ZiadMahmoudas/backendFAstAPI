import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# قراءة الـ DATABASE_URL من Environment Variable
DATABASE_URL = os.getenv("DATABASE_URL")

# إعداد SSL لتجاوز مشاكل Vercel مع AsyncPG
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# إنشاء الـ Async Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"ssl": ssl_context}
)

# Session محلي
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base للـ Models
Base = declarative_base()

# Dependency للـ DB
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# إنشاء الـ Tables عند startup
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
