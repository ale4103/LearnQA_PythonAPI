import requests

class TestFirstAPI:
    def test_hello_call(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        expected_val = "<RequestsCookieJar[<Cookie HomeWork=hw_value for .playground.learnqa.ru/>]>"

        response = requests.post(url)
        actual_val = response.cookies

        print(actual_val)
        assert str(actual_val) == expected_val, f"Cookie values are not equal"