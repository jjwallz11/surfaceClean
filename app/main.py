from fastapi import FastAPI
from routes import router
from config import settings
import logging
from utils.db import engine, Base, AsyncSessionLocal
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func

# Seeding functions
from seeds import (
    seed_users,
    seed_machines,
    # seed_parts,  # Optional: temporarily disabled
    seed_images,
    seed_faqs,
    seed_testimonials,
)

# Models for table checks
from models.users import User
from models.machines import Machine
from models.images import Image
from models.faqs import FAQ
from models.testimonials import Testimonial
# from models.parts import Part  # Optional

app = FastAPI(title="Surface Clean API", debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:2911"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def seed_if_needed():
    async with AsyncSessionLocal() as db:
        # USERS
        count = await db.scalar(select(func.count()).select_from(User))
        if count == 0:
            logging.info("Seeding users...")
            await seed_users()

        # MACHINES
        count = await db.scalar(select(func.count()).select_from(Machine))
        if count == 0:
            logging.info("Seeding machines...")
            await seed_machines()

        # IMAGES
        count = await db.scalar(select(func.count()).select_from(Image))
        if count == 0:
            logging.info("Seeding images...")
            await seed_images()

        # FAQS
        count = await db.scalar(select(func.count()).select_from(FAQ))
        if count == 0:
            logging.info("Seeding FAQs...")
            await seed_faqs()

        # TESTIMONIALS
        count = await db.scalar(select(func.count()).select_from(Testimonial))
        if count == 0:
            logging.info("Seeding testimonials...")
            await seed_testimonials()

        # PARTS (optional)
        # count = await db.scalar(select(func.count()).select_from(Part))
        # if count == 0:
        #     logging.info("Seeding parts...")
        #     await seed_parts()


@app.on_event("startup")
async def startup_event():
    logging.info("Starting up the Surface Clean API")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if settings.ENVIRONMENT != "production":
        await seed_if_needed()
        logging.info("✅ Tables checked and seeded if needed")
    else:
        logging.info("🚫 Production environment detected; skipping seeding")


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down the Surface Clean API")


app.include_router(router)


@app.get("/")
def root():
    return {"message": "Welcome to Surface Clean API"}


if settings.ENVIRONMENT == "production":
    origins = ["https://yourdomain.com"]
else:
    origins = ["*"]