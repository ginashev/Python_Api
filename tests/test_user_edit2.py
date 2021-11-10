import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Edit user cases")
@allure.feature("EditUser")
class TestUserEdit(BaseCase):

    def test_edit_just_created_user_with_same_user(self):
        email, first_name, password, user_id, username = self.create_new_user()
        # LOGIN
        auth_sid, token, user_id1 = self.login(email, password)

        # EDIT
        edit_field = {"firstName": "new_name"}
        self.edit_user_data_field(auth_sid, edit_field, token, user_id, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            edit_field["firstName"],
            "Wrong name of the user after edit"
        )

    def test_edit_just_user_created_user_with_not_auth(self):
        email, first_name, password, user_id, username = self.create_new_user()

        # LOGIN
        auth_sid, token, user_id1 = self.login(email, password)

        # EDIT
        edit_field = {"firstName": "new_name"}
        response3 = self.edit_user_data_field(None, edit_field, None, user_id, 400)

        assert response3.content.decode("utf-8") == f"Auth token not supplied", \
            f"Unexpected response content {response3.content}"

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name,
            "Non authorize user cannot change name"
        )

    def test_edit_just_created_user_with_different_user(self):
        # REGISTER
        email, first_name, password, user_id, username = self.create_new_user()

        # LOGIN
        auth_sid, token, user_id1 = self.login('vinkotov@example.com', '1234')

        # EDIT
        edit_field = {"username": "new_username"}
        response3 = self.edit_user_data_field(auth_sid, edit_field, token, user_id, 400)
        assert response3.content.decode("utf-8") == f"Please, do not edit test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response3.content}"

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "username",
            username,
            "Wrong name of the user after edit"
        )

    def test_edit_to_incorrect_name_just_created_user_with_same_user(self):
        # REGISTER
        email, first_name, password, user_id, username = self.create_new_user()

        # LOGIN
        auth_sid, token, user_id1 = self.login(email, password)

        # EDIT
        new_name = "a"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Too short value for field firstName",
            "Incorrect error message"
        )

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name,
            "Wrong name of the user after edit"
        )

    def test_edit_email_just_created_user_with_same_user(self):
        # REGISTER
        email, first_name, password, user_id, username = self.create_new_user()

        # LOGIN
        auth_sid, token, user_id1 = self.login(email, password)

        # EDIT
        edit_field = {"email": "vinkotov.example.com"}
        response3 = self.edit_user_data_field(auth_sid, edit_field, token, user_id, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response3.content}"

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "email",
            email,
            "Wrong name of the user email edit"
        )
