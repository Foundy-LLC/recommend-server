import os

from dotenv import load_dotenv

load_dotenv()


class ConnectConfig:
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", 8000)
    DB_DATABASE: str = os.getenv("DB_DATABASE")

    DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"


connect_config = ConnectConfig()
