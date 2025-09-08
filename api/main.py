from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from api.database import engine, Base
from api.routers import heroes

app = FastAPI(title="Heroes API (Async)", version="6.0")
app.include_router(heroes.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إنشاء الـ Tables عند startup
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# @app.on_event("startup")
# async def on_startup():
#     await init_models()

# handler = Mangum(app)