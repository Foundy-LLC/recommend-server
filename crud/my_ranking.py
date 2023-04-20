from sqlalchemy import text
from sqlalchemy.orm import Session


def get_my_ranking(db: Session, user_id: str, weekly: bool):
    criteria_score = "weekly_score" if weekly else "total_score"
    criteria_ranking = "weekly_ranking" if weekly else "total_ranking"

    query = f"""
    WITH
        inquiry AS (select user_id as user_id, \
        {criteria_score} as score, {criteria_ranking} as ranking from user_ranking where user_id='{user_id}')

    
    select id, name, profile_image as profileImage, ranking.score as rankingScore, ranking.ranking as ranking, status
    from user_account
    join (
        table inquiry
    ) as ranking
    on ranking.user_id = user_account.id
    """

    query_result = db.execute(text(query))

    return [data for data in query_result]
