import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Settings:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'changeme'
    ALGORITHM = os.environ.get('ALGORITHM') or 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES') or 30)
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT') or 5000
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
        if os.environ.get('DATABASE_URL') else 'sqlite:///./test.db'
    )
    SQLALCHEMY_ECHO = True