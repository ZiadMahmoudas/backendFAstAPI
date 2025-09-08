import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres.wqvtwctdjevzldwpderu:0123456789Ziad@aws-1-eu-north-1.pooler.supabase.com:6543/postgres"
)

# Create synchronous SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True  # optional, for SQLAlchemy 2.0 style
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Base for models
Base = declarative_base()

# ========================
# Helper functions
# ========================
def get_db():
    """Synchronous DB session generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_models():
    """Create tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables initialized successfully!")
