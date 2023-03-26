from sqlalchemy import text
from sqlalchemy.orm import Session

LIMIT = 50


def get_all_ranking(db: Session, organizationId: int, page: int):
    query = f"""
    select id, name, profile_image as profileImage, ranking.total_score as rankingScore, status
    from user_account
    join (
        select user_id, total_score from user_ranking
        order by total_score
    ) as ranking
    on ranking.user_id = user_account.id 
    """

    if organizationId:
        orgs_q = db.execute(text('select id from organization'))
        orgs = [int(org[0]) for org in orgs_q]

        if organizationId not in orgs:
            return "NO ORG"

        query = f"""
        select total.id, total.name, total.profileImage, total.rankingScore, total.status
        from ({query}) as total
        join belong on total.id = belong.user_id
        where belong.organization_id='{organizationId}'
        """
    query += f"""
    limit {LIMIT}
    offset {page * LIMIT}
    """

    query_result = db.execute(text(query))

    return [data for data in query_result]
