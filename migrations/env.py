from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Import Base after .env is loaded
from app.models.db import Base
from app.models import *  # All models must be imported for autogenerate to work

# Alembic Config
config = context.config
fileConfig(config.config_file_name)

# Override URL with SYNC version
raw_async_url = os.getenv("DATABASE_URL")
if raw_async_url is None:
    raise Exception("DATABASE_URL environment variable is not set")
if raw_async_url.startswith("sqlite+aiosqlite://"):
    sync_url = raw_async_url.replace("sqlite+aiosqlite://", "sqlite://")
else:
    raise Exception(f"Only sqlite+aiosqlite:// is currently supported for fallback, got: {raw_async_url}")

config.set_main_option("sqlalchemy.url", sync_url)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()