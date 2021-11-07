from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_cookie_value_by_name(response: Response, cookie_name, expected_value, error_message):
        assert cookie_name in response.cookies, f"Cannot find cookie with name{cookie_name}"
        assert response.cookies[cookie_name] == expected_value, error_message

    @staticmethod
    def assert_header_value_by_name(response: Response, header_name, expected_value, error_message):
        assert header_name in response.headers, f"Cannot find cookie with name{header_name}"
        assert response.headers[header_name] == expected_value, error_message
