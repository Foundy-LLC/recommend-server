from sqlalchemy import text
from sqlalchemy.orm import Session


def get_users_count(db: Session, organizationId=None):
    query = f"""
    select count(*) from user_account
    """

    if organizationId:
        query += f"""
        join belong b on user_account.id = b.user_id
        and b.organization_id='{organizationId}'
        and b.is_authenticated=true
        """

    query_result = db.execute(text(query))

    return int(query_result.scalar())


def is_user_valid(db: Session, user_id: str):
    query = f"""
    select exists (
        select 1 from user_account
        where id='{user_id}'
    )
    """

    result = db.execute(text(query)).scalar()

    return result
