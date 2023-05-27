from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import connect_config

SQLALCHEMY_DATABASE_URL = connect_config.DATABASE_URL

# DB 연결 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_size=10,
                       max_overflow=20,
                       pool_recycle=900,
                       pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
