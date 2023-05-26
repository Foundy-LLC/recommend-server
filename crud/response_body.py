from typing import Tuple, Dict

from fastapi import status as st_code

import apis.response_config as config


def get_response_body(user_cnt: int, result: list, is_personal=False) -> Tuple[int, Dict]:
    res_body = config.ResponseConfig()

    if not result:
        return st_code.HTTP_404_NOT_FOUND, res_body.out_of_page()
    elif result[0] == "NO ORG":
        return st_code.HTTP_404_NOT_FOUND, res_body.no_org()

    data = []

    for row in result:
        id, name, profile_image, score, rank, introduce, studyTime, status = row

        user_data = dict({
            "id": id,
            "name": name,
            "profileImage": profile_image,
            "rankingScore": score,
            "ranking": rank,
            "introduce": introduce,
            "studyTime": studyTime,
            "status": status,
        })

        data.append(user_data)

    if is_personal:
        return st_code.HTTP_200_OK, res_body.success(user_cnt=user_cnt, data=data[0])
    return st_code.HTTP_200_OK, res_body.success(user_cnt=user_cnt, data=data)

def get_recommend_response_body(result:list) -> Tuple[int, dict]:
    pass
