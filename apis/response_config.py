from fastapi import status


class ResponseConfig:
    def __init__(self):
        self.message = ""
        self.data = None
        self.status = None
        self.response_body = {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }

    def update(self, data: dict):
        self.response_body["status"] = data["status"] or None
        self.response_body["message"] = data["message"] or None
        self.response_body["data"] = data["data"] or None

    def success(self, data):
        self.message = "회원 랭킹을 성공적으로 얻었습니다."
        self.data = data
        self.status = status.HTTP_200_OK

        new_data = {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }

        self.update(new_data)
        return self.response_body

    def no_org(self):
        self.status = status.HTTP_404_NOT_FOUND
        self.message = "소속이 존재하지 않습니다."

        new_data = {
            "status": self.status,
            "message": self.message,
        }
        self.update(new_data)
        return self.response_body

    def out_of_page(self):
        self.status = status.HTTP_404_NOT_FOUND
        self.message = "더 이상 랭킹이 존재하지 않습니다."

        new_data = {
            "status": self.status,
            "message": self.message,
        }
        self.update(new_data)
        return self.response_body
