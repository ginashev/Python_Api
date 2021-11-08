import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestHomeCookie(BaseCase):

    def test_home_cookie(self):
        response1 = requests.get("https://playground.learnqa.ru/api/homework_header")
        header = response1.headers
        print(header)
        headers = {'Content-Type': 'application/json', 'Content-Length': '15'}
        for key, value in headers.items():
            Assertions.assert_header_value_by_name(
                response1,
                key,
                value,
                f"header '{key}' value not equal '{value}'"
            )
