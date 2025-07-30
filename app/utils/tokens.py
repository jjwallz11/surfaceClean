# app/utils/tokens.py

from itsdangerous import URLSafeTimedSerializer
from config import settings

serializer = URLSafeTimedSerializer(settings.JWT_SECRET)

def create_reset_token(user_id: int) -> str:
    return serializer.dumps({"user_id": user_id}, salt="password-reset")

def verify_reset_token(token: str, max_age: int = 3600):
    try:
        data = serializer.loads(token, salt="password-reset", max_age=max_age)
        return data["user_id"]
    except Exception:
        return None