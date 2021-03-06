from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import allure


@allure.epic("Get user cases")
@allure.feature("GEtUserInfo")
class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, expected_fields)

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_different_user(self):
        new_user_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=new_user_data)
        id = self.get_json_value(response1, "id")

        old_user_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=old_user_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        response2 = MyRequests.get(f"/user/{id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, expected_fields)
