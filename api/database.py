import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlalchemy.pool

# ====== إعداد رابط قاعدة البيانات ======
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres.wqvtwctdjevzldwpderu:0123456789Ziad@aws-1-eu-north-1.pooler.supabase.com:6543/postgres?sslmode=require"
)

print("DATABASE_URL:", DATABASE_URL)

# ====== إعداد SSL لتخطي مشاكل التحقق من الشهادة ======
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE  # فقط للتجريب المحلي

# ====== إنشاء محرك قاعدة البيانات ======
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    poolclass=sqlalchemy.pool.NullPool,  # لتجنب مشاكل pgbouncer و DuplicatePreparedStatement
    connect_args={
        "ssl": ssl_context,
        "statement_cache_size": 0  # مهم لتجنب DuplicatePreparedStatementError
    }
)

# ====== إنشاء Session ======
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ====== Base للـ ORM ======
Base = declarative_base()

# ====== دالة للحصول على session ======
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ====== دالة لإنشاء الجداول ======
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


