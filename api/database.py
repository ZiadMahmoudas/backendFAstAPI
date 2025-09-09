from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

# DATABASE_URL = "mysql+aiomysql://sql8797878:9NFsqGi8Ib@sql8.freesqldatabase.com:3306/sql8797878"
DATABASE_URL = "postgresql+asyncpg://postgres.wqvtwctdjevzldwpderu:0123456789Ziad@aws-1-eu-north-1.pooler.supabase.com:6543/postgres"

# إنشاء engine غير متزامن
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# إعداد الجلسة
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# قاعدة البيانات ORM
Base = declarative_base()

# تعريف نموذج Hero
class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  
    name = Column(String, nullable=False)
    power = Column(String, nullable=False)

# دالة للحصول على الجلسة
async def get_db():
    """إرجاع الجلسة غير المتزامنة لقاعدة البيانات"""
    async with AsyncSessionLocal() as session:
        yield session

# دالة لتهيئة الجداول في قاعدة البيانات
async def init_models():
    """إنشاء الجداول في قاعدة البيانات"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ تم تهيئة الجداول بنجاح!")
