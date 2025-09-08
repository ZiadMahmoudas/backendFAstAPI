# api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.database import engine, Base
from api.routers import heroes

app = FastAPI(title="Heroes API (Async)", version="6.0")

# 🔴 تأكد من أن CORSMiddleware هي أول شيء
# إذا كنت تنوي استخدامها
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔴 ثم قم بتضمين الـ router
app.include_router(heroes.router)

# إنشاء الـ Tables عند startup
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 🔴 استخدم lifespan بدلاً من on_event
@app.on_event("startup")
async def on_startup():
    await init_models()