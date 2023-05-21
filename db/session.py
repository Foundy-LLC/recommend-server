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

"""
세션 생성

autocommit : DB 의 내용이 변경된 경우 자동으로 commit 하여 변경할지에 대한 여부를 결정
False 로 지정된 경우 insert, update, delete 등 작업이 일어났을 때 수동으로 commit 해줘야한다.

autoflush : commit 되지 않은 부분을 자동으로 삭제할지에 대한 여부
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
