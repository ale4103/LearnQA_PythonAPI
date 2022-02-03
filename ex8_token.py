import requests
import json
import time

# 1. create task
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print(response.text)

# parsing answer to get token and time
json_load = json.loads(response.text)
token = json_load["token"]
seconds = json_load["seconds"]

# 2. check status before task is ready
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":token})
print(response.text)

# 3. wait
time.sleep(seconds)

# 4. check status when task is ready
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":token})
print(response.text)

