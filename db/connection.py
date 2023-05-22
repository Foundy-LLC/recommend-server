import time

from db.session import SessionLocal


def connect_db():
    db = SessionLocal()
    is_error = True  # 데이터 베이스에서 오류가 있는 경우 재시도 할 수 있도록 함
    retry_count = 0

    while is_error:
        try:
            is_error = False
            yield db

        except Exception:
            if retry_count > 5:
                print("DB POOL EXCEEDED")
                is_error = False  # 무한 시도 방지

            time.sleep(1.5)
            retry_count += 1

        finally:
            db.close()
