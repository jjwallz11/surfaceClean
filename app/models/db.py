# app/models/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from app.config import settings

# Check if we're in sync mode for seeding
if os.environ.get('USE_SYNC_DB') == 'true':
    # Use sync engine for seeding
    sync_database_url = settings.DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite://")
    engine = create_engine(sync_database_url, echo=True)
    SessionLocal = sessionmaker(bind=engine)
else:
    # Use async engine for normal operations
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
