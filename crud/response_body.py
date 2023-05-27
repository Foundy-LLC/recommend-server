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
    res_body = config.ResponseConfig(for_recommend=True)

    if not result:
        return st_code.HTTP_400_BAD_REQUEST, res_body.invalid_uid()

    friends = []

    for row in result:
        u_id, name, profileImage, introduce, status, similarity = row

        user_data = dict({
            "id": u_id,
            "name": name,
            "similarity" : f"{similarity*100:.2f}%",
            "profileImage" : profileImage,
            "introduce": introduce,
            "status": status
        })

        friends.append(user_data)

    return st_code.HTTP_200_OK, res_body.success(user_cnt=len(friends), data=friends)