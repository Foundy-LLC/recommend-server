from sqlalchemy import text
from sqlalchemy.orm import Session


def get_my_total_ranking(db: Session, user_id: str, weekly: bool):
    criteria_score = "weekly_score" if weekly else "total_score"
    criteria_ranking = "weekly_ranking" if weekly else "total_ranking"
    criteria_study_time = "weekly_study_time" if weekly else "total_study_time"

    query = f"""
    WITH
        inquiry AS (select user_id as user_id, \
        {criteria_score} as score, {criteria_ranking} as ranking,\
        {criteria_study_time} as studyTime from user_ranking where user_id='{user_id}')

    
    select id, name, profile_image as profileImage, ranking.score as rankingScore, ranking.ranking as ranking,\
     introduce, ranking.studyTime, status
    from user_account
    left outer join (
        table inquiry
    ) as ranking
    on ranking.user_id = user_account.id
    """

    query_result = db.execute(text(query))

    return [data for data in query_result]


def get_my_org_ranking(db: Session, user_id: str, organizationId: int):
    orgs_q = db.execute(text('select id from organization'))
    orgs = [int(org[0]) for org in orgs_q]

    if organizationId not in orgs:
        return ["NO ORG"]

    query = f"""
    select * from 
    (select total.id, name, total.profileImage, total.rankingScore, \
    rank() over (order by coalesce(total.rankingScore, 0) desc) as ranking,\
    total.introduce, total.studyTime, total.status
    from
    (
        select id, name, profile_image as profileImage, coalesce(ranking.total_score,0) as rankingScore,\
        introduce, coalesce(ranking.total_study_time,0) as studyTime, status
        from user_account
        left outer join (
            select user_id, total_score, total_study_time from user_ranking
        ) as ranking
        on ranking.user_id = user_account.id
    ) as total
    join belong
    on belong.organization_id='{organizationId}') as final
    where final.id = '{user_id}'
    """

    query_result = db.execute(text(query))

    return [data for data in query_result]
