from fastapi import APIRouter
from app.schemas.example import ExampleSchema

router = APIRouter()

@router.get("/example")
def get_example():
    return {"message": "Example endpoint"}

@router.post("/example")
def create_example(data: ExampleSchema):
    return {"received": data}