import apis.response_config as config
from crud import all_ranking


# id, name, profile_image as profileImage, ranking.total_score as rankingScore, status

def ranking_index(db, organization: str, page: int):
    result = all_ranking.get_all_ranking(db, organization=organization, page=page)
    data = {"users": []}

    for row in result:
        id, name, profile_image, score, status = row

        user_data = dict({
            "id": id,
            "name": name,
            "profileImage": profile_image,
            "rankinScore": score,
            "status": status
        })

        data["users"].append(user_data)

    res_body = config.ResponseConfig()
    return res_body.success(data)
