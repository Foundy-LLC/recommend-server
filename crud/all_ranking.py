from sqlalchemy import text
from sqlalchemy.orm import Session


def get_all_items(db: Session):
    query = text('select name, address from organization')
    res = db.execute(query)

    return [{"School": row[0], "email": row[1]} for row in res]


def get_all_ranking(db: Session, organization: str, page: int):
    LIMIT = 50

    query = f"""
    select id, name, profile_image as profileImage, ranking.total_score as rankingScore, status
    from user_account
    join (
        select user_id, total_score from user_ranking
        order by total_score
        limit {LIMIT} 
        offset {(page - 1) * LIMIT}
    ) as ranking
    on ranking.user_id = user_account.id 
    """

    res = db.execute(text(query))

    ret = []
    for cursor in res:
        ret.append(cursor)

    return ret
