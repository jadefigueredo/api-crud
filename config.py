import os
import dotenv import load_dotenv

load_dotenv()

class Config:
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    
    SQLALCHEMY_DATABASE_URI = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/clothings"
                               )
    SQLALCHEMY_TRACK_MODIFICATIONS = False