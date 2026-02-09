#import os
#from dotenv import load_dotenv

#load_dotenv()

#DB_HOST = os.getenv("DB_HOST")
#DB_NAME = os.getenv("DB_NAME")
#DB_USER = os.getenv("DB_USER")
#DB_PASS = os.getenv("DB_PASS")

#JWT_SECRET = os.getenv("JWT_SECRET")

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    JWT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
