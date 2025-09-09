from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import heroes
from api.database import init_models

app = FastAPI(title="Heroes API (Async)", version="6.0")

app.include_router(heroes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# دالة لتبدأ تشغيل الجداول عند بدء التطبيق
@app.on_event("startup")
async def startup():
    print("Initializing the database tables...")
    await init_models()  # تهيئة الجداول عند بدء التطبيق

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
