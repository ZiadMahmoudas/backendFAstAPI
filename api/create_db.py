import asyncio
from api.database import init_models
from api.database import engine, Base

async def create_tables():
    print("جاري إنشاء جداول قاعدة البيانات...")
    await init_models()
    print("✅ تم إنشاء الجداول بنجاح!")

if __name__ == "__main__":
    asyncio.run(create_tables())