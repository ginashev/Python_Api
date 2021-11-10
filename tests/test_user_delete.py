import pytest
import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Delete user cases")
@allure.feature("DeleteUser")
class TestUserDelete(BaseCase):

    def test_delete_exist_user_negative(self):
        # LOGIN
        auth_sid, token, user_id = self.login('vinkotov@example.com', '1234')

        # DELETE
        response = self.delete_user(auth_sid, token, user_id, 400)
        assert response.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response.content}"

        # GET
        response2 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response2,
            "username",
            "Vitaliy",
            "User not found"
        )

    def test_delete_new_user_positive(self):
        # REGISTER
        email, first_name, password, user_id, username = self.create_new_user()

        # LOGIN
        auth_sid, token, user_id = self.login(email, password)

        # DELETE
        self.delete_user(auth_sid, token, user_id, 200)

        # GET
        response = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        assert response.content.decode("utf-8") == f"User not found", \
            f"Unexpected response content {response.content}"

    def test_delete_new_user_negative(self):
        # REGISTER
        email, first_name, password, user_id1, username = self.create_new_user()

        # LOGIN
        auth_sid, token, user_id = self.login('vinkotov@example.com', '1234')

        # DELETE
        response1 = self.delete_user(auth_sid, token, user_id1, 400)
        assert response1.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response1.content}"
        # GET
        response2 = MyRequests.get(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response2,
            "username",
            username,
            "User not found"
        )
