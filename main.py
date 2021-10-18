from json.decoder import JSONDecodeError
import requests

response = ""

methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
for met in methods:
    if met == "GET":
        response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": met})
        print(met + response.text)
    if met == "POST":
        response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": met})
        print(met + response.text)
    if met == "PUT":
        response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": met})
        print(met + response.text)
    if met == "DELETE":
        response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": met})
        print(met + response.text)
    if met == "HEAD":
        response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
        print(met + response.text)
