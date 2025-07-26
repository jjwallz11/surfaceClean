# app/seeds/users.py

from app.models import User
from sqlalchemy.orm import Session
from app.utils.auth import get_password_hash

def seed_users(db: Session):
    users = [
        User(
            email="jjparedez3@gmail.com",
            first_name="Johnny",
            last_name="Paredez III",
            hashed_password=get_password_hash("BAtFitFMA13#*")
        ),
        User(
            email="surfaceclean111@yahoo.com",
            first_name="Dave",
            last_name="Siano",
            hashed_password=get_password_hash("password")
        ),
    ]

    db.add_all(users)

def undo_users(db: Session):
    db.query(User).delete()