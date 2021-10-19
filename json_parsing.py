import json


def get_key_from_json(string, key):
    json_obj = json.loads(string)
    if key in json_obj:
        return json_obj[key]
    else:
        return f"No key {key} in JSON"
