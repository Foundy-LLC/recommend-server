from sqlalchemy import text
from sqlalchemy.orm import Session


def get_items(db: Session):
    query = text('select name, address from organization')
    res = db.execute(query)

    return [{"School": row[0], "email": row[1]} for row in res]
