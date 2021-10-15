from json.decoder import JSONDecodeError
import requests


response = requests.get(" https://playground.learnqa.ru/api/long_redirect")
print(len(response.history)-1)
print(response.url)