import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(response.history, response.url)