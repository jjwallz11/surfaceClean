# app/main.py
from fastapi import FastAPI
from routes import router
from config import settings
import logging
from utils.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from seeds.cli import seed_all_async

app = FastAPI(title="Surface Clean API", debug=settings.DEBUG)

origins = ["https://yourdomain.com"] if settings.ENVIRONMENT == "production" else ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.on_event("startup")
async def startup_event():
    logging.info("Starting up the Surface Clean API")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        await seed_all_async()
        logging.info("✅ Seeding run finished (idempotent).")
    except Exception as e:
        logging.exception(f"Seed step skipped/failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down the Surface Clean API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to Surface Clean API"}