# app/scripts/seed.py

import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.seeds import (
    seed_users, undo_users,
    seed_machines, undo_machines,
    seed_parts, undo_parts,
    seed_images, undo_images,
    seed_faqs, undo_faqs,
    seed_testimonials, undo_testimonials
)
from app.models.db import Base

# Ensure project root is in sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

print("🌱 Seeding database...")

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def run_seeds():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Unseed in reverse order
    undo_testimonials(session)
    undo_faqs(session)
    undo_images(session)
    # undo_parts(session)
    undo_machines(session)
    undo_users(session)

    # Seed in forward order
    seed_users(session)
    seed_machines(session)
    # seed_parts(session)
    seed_images(session)
    seed_faqs(session)
    seed_testimonials(session)

    session.commit()
    print("✅ Done seeding.")

if __name__ == "__main__":
    run_seeds()