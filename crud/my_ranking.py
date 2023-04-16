from sqlalchemy import text
from sqlalchemy.orm import Session


def get_total_ranking(db: Session, user_id):
    query = f"""
    select id, name, profile_image as profileImage, ranking.total_score as rankingScore, status
    from user_account
    join (
        select user_id, total_score from user_ranking
        where user_id='{user_id}'
    ) as ranking
    on ranking.user_id = user_account.id
    """

    query_result = db.execute(text(query))

    return [data for data in query_result]
