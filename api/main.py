from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import heroes
from api.database import init_models
import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="Heroes API (Async)", version="6.0")

app.include_router(heroes.router)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://localhost:4200","https://shiny-gingersnap-ea19b6.netlify.app"],
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# دالة لتبدأ تشغيل الجداول عند بدء التطبيق
@app.on_event("startup")
async def startup():
    try:
        logging.debug("Initializing the database tables...")
        await init_models()  # تهيئة الجداول عند بدء التطبيق
    except Exception as e:
        logging.error(f"Error during startup: {e}")



@app.get("/")
def read_root():
    return {"message": "Hello World"}
