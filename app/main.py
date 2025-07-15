from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import example  # adjust import if layout is different

app = FastAPI()

# CORS settings
origins = ["http://localhost:5173"]  # Vite dev server port
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(example.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API is running"}