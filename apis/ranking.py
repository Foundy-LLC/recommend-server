from crud.all_ranking import get_all_ranking, get_org_ranking
from crud.my_ranking import get_my_total_ranking, get_my_org_ranking
from crud.response_body import get_response_body


def ranking_total(db, weekly: bool, page: int):
    result = get_all_ranking(db, weekly=weekly, page=page)
    return get_response_body(result)


def ranking_organization(db, organizationId: int, page: int):
    result = get_org_ranking(db, organizationId, page=page)
    return get_response_body(result)


def personal_total_ranking(db, user_id: str, weekly: bool):
    result = get_my_total_ranking(db, user_id, weekly)
    return get_response_body(result, is_personal=True)


def personal_org_ranking(db, user_id: str, organizationId: int):
    result = get_my_org_ranking(db, user_id, organizationId)
    return get_response_body(result, is_personal=True)
