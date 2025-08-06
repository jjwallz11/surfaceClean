# app/main.py

from fastapi import FastAPI
from routes import router
from config import settings
import logging
from utils.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Surface Clean API", debug=settings.DEBUG)

if settings.ENVIRONMENT == "production":
    origins = ["https://yourdomain.com"]
else:
    origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

@app.on_event("startup")
async def startup_event():
    logging.info("Starting up the Surface Clean API")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logging.info("✅ Tables checked (no seeding run)")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down the Surface Clean API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to Surface Clean API"}