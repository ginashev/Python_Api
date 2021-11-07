import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestHomeCookie(BaseCase):
    def test_home_cookie(self):
        response1 = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        Assertions.assert_cookie_value_by_name(
            response1,
            "HomeWork",
            "hw_value",
            "Cookie value not equal 'hm_value'"
        )
