import random
import string

import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotov.example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    empty_field = [
        "password",
        "username",
        "firstName",
        "lastName",
        "email"
    ]

    @pytest.mark.parametrize('empty_field', empty_field)
    def test_create_user_with_out_one_required_field(self, empty_field):
        data = self.prepare_registration_data()
        data[empty_field] = None
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {empty_field}", \
            f"Unexpected response content {response.content}"

    name_len = [
        1,
        255,
    ]

    @pytest.mark.parametrize('name_len', name_len)
    def test_create_user_with_incorrect_name_len(self, name_len):
        first_name = 'firstName'
        data = self.prepare_registration_data()
        data[first_name] = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=name_len))
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        if name_len < 255:
            assert response.content.decode("utf-8") == f"The value of '{first_name}' field is too short", \
                f"Unexpected response content {response.content}"
        else:
            assert response.content.decode("utf-8") == f"The value of '{first_name}' field is too long", \
                f"Unexpected response content {response.content}"
