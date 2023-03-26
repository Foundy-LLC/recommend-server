from fastapi import status as st_code

import apis.response_config as config
from crud import all_ranking


def ranking_total(db, organizationId: int, page: int):
    result = all_ranking.get_all_ranking(db, organizationId=organizationId, page=page)
    res_body = config.ResponseConfig()

    if not result:
        return st_code.HTTP_404_NOT_FOUND, res_body.out_of_page()
    elif result == "NO ORG":
        return st_code.HTTP_404_NOT_FOUND, res_body.no_org()

    data = []

    for row in result:
        id, name, profile_image, score, status = row

        user_data = dict({
            "id": id,
            "name": name,
            "profileImage": profile_image,
            "rankingScore": score,
            "status": status
        })

        data.append(user_data)

    return st_code.HTTP_200_OK, res_body.success(data)
