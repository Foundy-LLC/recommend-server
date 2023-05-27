class ResponseConfig:
    def __init__(self, for_recommend=False):
        self.message = ""
        self.data = None
        self.recommend = for_recommend
        self.response_body = {
            "message": self.message,
            "data": self.data
        }

    def update(self, data: dict):
        self.response_body["message"] = data["message"] or None
        self.response_body["data"] = data["data"] or []

    def success(self, data, user_cnt, rec_type="친구"):
        if self.recommend:
            self.message = f"추천 {rec_type} 목록을 성공적으로 얻었습니다."
        else:
            self.message = "회원 랭킹을 성공적으로 얻었습니다."

        self.data = data

        if rec_type == "친구":
            total = "totalUserCount"
            data_type = "users"
        else:
            total = "totalRoomCount"
            data_type = "rooms"

        new_data = {
            "message": self.message,
            "data": {total: user_cnt, data_type: self.data}
        }

        self.update(new_data)
        return self.response_body

    def no_org(self):
        self.message = "소속이 존재하지 않습니다."

        new_data = {
            "message": self.message,
            "data": []
        }

        self.update(new_data)
        return self.response_body

    def out_of_page(self):
        self.message = "더 이상 랭킹이 존재하지 않습니다."

        new_data = {
            "message": self.message,
            "data": []
        }
        self.update(new_data)
        return self.response_body

    def invalid_uid(self):
        self.message = "UID가 누락되거나 유효하지 않은 UID입니다."

        new_data = {
            "message": self.message,
            "data": []
        }

        self.update(new_data)
        return self.response_body
