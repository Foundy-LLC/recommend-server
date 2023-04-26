class ResponseConfig:
    def __init__(self):
        self.message = ""
        self.data = None
        self.response_body = {
            "message": self.message,
            "data": self.data
        }

    def update(self, data: dict):
        self.response_body["message"] = data["message"] or None
        self.response_body["data"] = data["data"] or []

    def success(self, data, user_cnt):
        self.message = "회원 랭킹을 성공적으로 얻었습니다."
        self.data = data

        new_data = {
            "message": self.message,
            "data": {"totalUserCount": user_cnt, "users": self.data}
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
