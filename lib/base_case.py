from datetime import datetime
import json.decoder
from lib.my_requests import MyRequests
from requests import Response
from lib.assertions import Assertions


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name '{cookie_name}'"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name '{headers_name}'"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def edit_user_data_field(self, auth_sid, edit_field, token, user_id, code):
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=edit_field
        )
        Assertions.assert_code_status(response, code)
        return response

    def login(self, email, password):
        login_data = {
            'email': email,
            'password': password
        }
        response = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id = self.get_json_value(response, "user_id")
        return auth_sid, token, user_id

    def create_new_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")
        user_name = register_data['username']
        return email, first_name, password, user_id, user_name

    def delete_user(self, auth_sid, token, user_id, code):
        response = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response, code)
        return response
