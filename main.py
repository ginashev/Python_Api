from json.decoder import JSONDecodeError
import requests

response = ""

methods = ["POST", "GET", "PUT", "DELETE", "HEAD"
           ]
for met in methods:
    if met == "POST":
        response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": met})
        print(response.url)
        print(response.text)
    if met == "GET":
        response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": met})
        print(response.url)
        print(response.text)
    if met == "PUT":
        response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": met})
        print(response.url)
        print(response.text)
    if met == "DELETE":
        response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": met})
        print(response.url)
        print(response.text)
    else:
        response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": met})
        print(response.url)
        print(response.text)
