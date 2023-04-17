from crud.all_ranking import get_all_ranking, get_org_ranking
from crud.my_ranking import get_total_ranking
from crud.response_body import get_response_body


def ranking_total(db, weekly: bool, page: int):
    result = get_all_ranking(db, weekly=weekly, page=page)
    return get_response_body(result)


def ranking_organization(db, organizationId: int, page: int):
    result = get_org_ranking(db, organizationId, page=page)
    return get_response_body(result)


def personal_ranking(db, user_id: str):
    result = get_total_ranking(db, user_id)
    return get_response_body(result, is_personal=True)
