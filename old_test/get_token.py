import requests
import json
import time


def get_key_from_json(string, key):
    json_obj = json.loads(string)
    if key in json_obj:
        return json_obj[key]
    else:
        return f"No key {key} in JSON"


response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print(response1.text)
seconds = get_key_from_json(response1.text, "seconds")
token = get_key_from_json(response1.text, "token")
response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
print(response2.text)
status1 = get_key_from_json(response2.text, "status")
assert status1 == "Job is NOT ready"
time.sleep(int(seconds))
response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
status2 = get_key_from_json(response3.text, "status")
print(response3.text)
assert status2 == "Job is ready"
