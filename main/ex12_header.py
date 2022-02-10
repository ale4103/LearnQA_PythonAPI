import requests

class TestFirstAPI:
    def test_hello_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        expected_val = 'Some secret value'

        response = requests.post(url)
        actual_val = response.headers['x-secret-homework-header']

        print(response.headers)
        assert actual_val == expected_val, f"В ответе нет заголовка x-secret-homework-header"