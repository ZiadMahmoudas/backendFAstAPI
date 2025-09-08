import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres.wqvtwctdjevzldwpderu:0123456789Ziad"
    "@aws-1-eu-north-1.pooler.supabase.com:6543/postgres"
)

# Create asynchronous SQLAlchemy engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base for models
Base = declarative_base()

# ========================
# Helper functions
# ========================
async def get_db():
    """Async DB session generator"""
    async with AsyncSessionLocal() as session:
        yield session

async def init_models():
    """Create tables asynchronously"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables initialized successfully!")
