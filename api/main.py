from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import heroes
from api.database import init_models
import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
app = FastAPI(title="Heroes API (Async)", version="6.0")

app.include_router(heroes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:4200","https://shiny-gingersnap-ea19b6.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # دالة لتبدأ تشغيل الجداول عند بدء التطبيق
# @app.on_event("startup")
# async def startup():
#     try:
#         logging.debug("Initializing the database tables...")
#         await init_models()  # تهيئة الجداول عند بدء التطبيق
#     except Exception as e:
#         logging.error(f"Error during startup: {e}")

async def create_tables():
    print("جاري إنشاء جداول قاعدة البيانات...")
    await init_models()
    print("✅ تم إنشاء الجداول بنجاح!")

if __name__ == "__main__":
    asyncio.run(create_tables())


@app.get("/")
def read_root():
    return {"message": "Hello World"}


