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


def get_rooms_response_body(result: list) -> Tuple[int, dict]:
    res_body = config.ResponseConfig(for_recommend=True)

    if result[0] == "INVALID_UID":
        return st_code.HTTP_400_BAD_REQUEST, res_body.invalid_uid()

    if not result:
        return st_code.HTTP_404_NOT_FOUND, res_body.out_of_page()

    rooms = []

    for row in result:
        room_id, title, master_id, has_password, thumbnail, overview_list, tags, similarity = row

        room_data = dict({
            "id": room_id,
            "title": title,
            "masterId": master_id,
            "hasPassword": has_password,
            "thumbnail": thumbnail,
            "joinCount": len(overview_list),
            "maxCount": 4,
            "joinedUsers": [{"id": over.id,
                             "name": over.name,
                             "profileImage": over.profileImage,
                             "introduce": over.introduce,
                             "status": over.status
                             } for over in overview_list],
            "tags": tags
        })

        rooms.append(room_data)

    return st_code.HTTP_200_OK, res_body.success(user_cnt=len(rooms), data=rooms, rec_type="방")


def get_recommend_response_body(result: list) -> Tuple[int, dict]:
    res_body = config.ResponseConfig(for_recommend=True)

    if not result:
        return st_code.HTTP_400_BAD_REQUEST, res_body.invalid_uid()

    friends = []

    for row in result:
        u_id, name, profileImage, introduce, status, similarity = row

        user_data = dict({
            "id": u_id,
            "name": name,
            "similarity": f"{similarity * 100:.2f}%",
            "profileImage": profileImage,
            "introduce": introduce,
            "status": status
        })

        friends.append(user_data)

    return st_code.HTTP_200_OK, res_body.success(user_cnt=len(friends), data=friends)
