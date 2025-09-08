# api/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔴 تأكد من أن هذا الرابط صحيح تمامًا
DATABASE_URL = os.getenv(
    "DATABASE_URL",
)

# 🔴 هذا هو الحل لمشكلة sslmode
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={
        "ssl": "require"
    }
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