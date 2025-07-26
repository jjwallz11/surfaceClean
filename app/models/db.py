# app/models/db.py
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

Base = declarative_base()
