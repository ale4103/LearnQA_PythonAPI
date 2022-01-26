import requests

response = requests.get("https://playground.learnqa.ru/api/hello")
print(response.text)

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)

print("Hello from Alexander!")