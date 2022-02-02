import json

string_as_json_format = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},' \
                        '{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
obj = json.loads(string_as_json_format)

key1 = "messages"
key2 = "message"

if key1 in obj:
    print(obj[key1][1][key2])
else:
    print(f"Ключа {key1} в JSON нет")