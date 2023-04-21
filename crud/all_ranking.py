from sqlalchemy import text
from sqlalchemy.orm import Session

LIMIT = 50


def get_all_ranking(db: Session, weekly: bool, page: int):
    criteria_score = "weekly_score" if weekly else "total_score"

    query = f"""
    WITH
        rank_result AS (select user_id as user_id, {criteria_score} as score from user_ranking)

    select id, name, profile_image as profileImage, ranking.score as rankingScore, \
    rank() over (order by ranking.score desc) as ranking, status
    from user_account
    join (
        table rank_result
    ) as ranking
    on ranking.user_id = user_account.id 
    order by ranking
    """

    query += f"""
    limit {LIMIT}
    offset {page * LIMIT}
    """

    query_result = db.execute(text(query))

    return [data for data in query_result]


def get_org_ranking(db: Session, organizationId: int, page: int):
    orgs_q = db.execute(text('select id from organization'))
    orgs = [int(org[0]) for org in orgs_q]

    if organizationId not in orgs:
        return ["NO ORG"]

    query = f"""
    select total.id, name, total.profileImage, total.rankingScore, \
    rank() over (order by total.rankingScore desc) as ranking, total.status
    from
    (
        select id, name, profile_image as profileImage, ranking.total_score as rankingScore, status
        from user_account
        join (
            select user_id, total_score from user_ranking
        ) as ranking
        on ranking.user_id = user_account.id
    ) as total
    join belong
    on total.id=belong.user_id
    and belong.organization_id='{organizationId}'
    """

    query += f"""
    limit {LIMIT}
    offset {page * LIMIT}
    """

    query_result = db.execute(text(query))

    return [data for data in query_result]
