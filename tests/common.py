import json


class MockReponse:
    def __init__(self, status_code: int, text: str):
        self.__status_code = status_code
        self.__text = text

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def text(self) -> str:
        return self.__text

    def json(self) -> dict:
        return json.loads(self.__text)
