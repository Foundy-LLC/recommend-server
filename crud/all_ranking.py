from sqlalchemy import text
from sqlalchemy.orm import Session

LIMIT = 50


def get_all_ranking(db: Session, weekly: bool, page: int):
    criteria_score = "weekly_score" if weekly else "total_score"
    criteria_study_time = "weekly_study_time" if weekly else "total_study_time"

    query = f"""
    WITH
        rank_result AS (select user_id as user_id, {criteria_score} as score,\
        {criteria_study_time} as studyTime from user_ranking)

    select id, name, profile_image as profileImage, coalesce(ranking.score,0) as rankingScore, \
    rank() over (order by coalesce(ranking.score,0) desc) as ranking, introduce,\
    coalesce(ranking.studyTime, 0) as studyTime, status
    from user_account
    left outer join (
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
    with total as (
        select id, name, profile_image as profileImage, coalesce(ranking.total_score, 0) as rankingScore,\
        introduce, coalesce(ranking.total_study_time, 0) as studyTime, status
        from user_account
        left outer join (
            select user_id, total_score, total_study_time from user_ranking
        ) as ranking
        on ranking.user_id = user_account.id
    )
    
    select only_auth.id, only_auth.name, only_auth.profileImage, only_auth.rankingScore, \
    rank() over (order by only_auth.rankingScore desc) as ranking, only_auth.introduce, only_auth.studyTime, only_auth.status
    from 
    (
        select total.id, total.name, total.profileImage, total.rankingScore, \
        total.introduce, total.studyTime, total.status
        from total
        join belong
        on total.id=belong.user_id
        and belong.organization_id='{organizationId}'
        and belong.is_authenticated=true) as only_auth
    """

    query += f"""
    limit {LIMIT}
    offset {page * LIMIT}
    """

    query_result = db.execute(text(query))

    return [data for data in query_result]
