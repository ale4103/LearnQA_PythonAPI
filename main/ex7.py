import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# http-запрос любого типа без параметра method
response = requests.get(url)
print(response.text)

# http-запрос не из списка
response = requests.head(url, params = {"method" : "GET"})
print(response.text)

# запрос с правильным значением method
response = requests.post(url, data = {"method" : "POST"})
print(response.text)

req = ["GET", "POST", "PUT", "DELETE"]
for value in req:
    response = requests.post(url, data = {"method" : value})
    print("post request,", f"method = {value}", "-", response.text)

print("-------------------------")
for value in req:
    response = requests.get(url, params={"method": value})
    print("get request,", f"method = {value}", "-", response.text)

print("-------------------------")
for value in req:
    response = requests.delete(url, params={"method": value})
    print("delete request,", f"method = {value}", "-", response.text)

print("-------------------------")
for value in req:
    response = requests.put(url, params={"method": value})
    print("put request,", f"method = {value}", "-", response.text)
