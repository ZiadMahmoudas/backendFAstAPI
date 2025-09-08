# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.database import init_models
from api.routers import heroes
from mangum import Mangum

app = FastAPI(title="Heroes API (Async)", version="6.0")

app.include_router(heroes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# async def on_startup():
#     print("Initializing database models...")
#     try:
#         await init_models()
#         print("Database initialized successfully.")
#     except Exception as e:
#         print("Error initializing database:", e)