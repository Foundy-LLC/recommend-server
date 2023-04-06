from crud import all_ranking
from crud.response_body import get_response_body


def ranking_total(db, page: int):
    result = all_ranking.get_all_ranking(db, page=page)
    return get_response_body(result)


def ranking_organization(db, organizationId: int, page: int):
    result = all_ranking.get_org_ranking(db, organizationId, page=page)
    return get_response_body(result)
