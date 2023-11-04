from dotenv import load_dotenv
from os import environ as env

load_dotenv()

DB_USER = env.get("DB_USER")
DB_PASSWORD = env.get("DB_PASSWORD")
DB_NAME = env.get("DB_NAME")
DB_HOST = env.get("DB_HOST")


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
