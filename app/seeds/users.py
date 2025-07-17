# seeds/users.py

from app.models import User
from app.db import get_db
from sqlalchemy.orm import Session
from utils.auth import get_password_hash 

def seed_users(db: Session):
    users = [
        User(
            email="jjparedez3@gmail.com",
            first_name="Johnny",
            last_name="Paredez III",
            hashed_password=get_password_hash("BAtFitFMA13#*")
        ),
        User(
            email="dave@dave.com",
            first_name="Dave",
            last_name="Siano",
            hashed_password=get_password_hash("password")
        ),
    ]

    db.add_all(users)
    db.commit()