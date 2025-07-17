from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    auth_router,
    users_router,
    machines_router,
    parts_router,
    images_router,
    testimonials_router,
    faqs_router
)

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(users_router, prefix="/api/users")
app.include_router(machines_router, prefix="/api/machines")
app.include_router(parts_router, prefix="/api/parts")
app.include_router(images_router, prefix="/api/images")
app.include_router(testimonials_router, prefix="/api/testimonials")
app.include_router(faqs_router, prefix="/api/faqs")

@app.get("/")
def root():
    return {"message": "API is running"}