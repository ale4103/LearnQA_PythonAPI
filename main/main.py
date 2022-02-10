from json.decoder import JSONDecodeError
import requests

# response = requests.get("https://playground.learnqa.ru/api/long_redirect")
# print(response.history)
# print(response.url)


payload = {"login":"secret_login", "password":"secret_pass"}
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

cookie_value = response1.cookies.get("auth_cookie")

cookies = {'auth_cookie': cookie_value}
if cookie_value is not None:
    cookies.update({"auth_cookie": cookie_value})

response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies = cookies)

print(response2.text)

# print(response.text)
# print(response.status_code)
# print(dict(response.cookies))
# print(response.headers)

'''
try:
    parsed_response_text = response.json()
    print(parsed_response_text)
except JSONDecodeError:
    print("Response is not a JSON format")
'''
'''
response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)

print("Hello from Alexander!")'''