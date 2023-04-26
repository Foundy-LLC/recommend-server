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
        """

    query_result = db.execute(text(query))

    return int(query_result.scalar())
