import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Delete cases")
class TestUserDelete(BaseCase):

    @allure.description("This test unsuccessfully delete user with id=2")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("positive_case")
    def test_delete_user_with_id2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert response2.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response for deletion user with ID 1, 2, 3, 4 or 5."

        response3 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})
        expected_fields = ["username", "firstName", "lastName", "email"]
        Assertions.assert_json_has_keys(response3, expected_fields)

    @allure.description("This test successfully delete created user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("positive_case")
    def test_delete_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Delete
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found", f"Unexpected response for getting deleted user"

    @allure.description("This test unsuccessfully delete user by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("negative_case")
    def test_delete_user_from_another_user(self):
        # Register user1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email1 = register_data1['email']
        first_name1 = register_data1['firstName']
        last_name1 = register_data1['lastName']
        password1 = register_data1['password']
        user_id1 = self.get_json_value(response1, "id")

        # Register user2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        email2 = register_data2['email']
        first_name2 = register_data2['firstName']
        password2 = register_data2['password']
        user_id2 = self.get_json_value(response2, "id")

        # Login user1
        login_data1 = {'email': email1, 'password': password1}
        response3 = MyRequests.post("/user/login", data=login_data1)
        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # Login user2
        login_data2 = {'email': email2, 'password': password2}
        response4 = MyRequests.post("/user/login", data=login_data2)
        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")

        # Delete
        response5 = MyRequests.delete(f"/user/{user_id1}",
                                      headers={'x-csrf-token': token2},
                                      cookies={'auth_sid': auth_sid2})

        Assertions.assert_code_status(response5, 200)

        # Get user1
        response6 = MyRequests.get(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
        )

        Assertions.assert_code_status(response6, 200)
        Assertions.assert_json_value_by_name(response6, "firstName", first_name1,
                                             "Wrong firstName of the user 1 after delete by another user")
        Assertions.assert_json_value_by_name(response6, "lastName", last_name1,
                                             "Wrong lastName of the user 1 after delete by another user")
        Assertions.assert_json_value_by_name(response6, "email", email1,
                                             "Wrong email of the user 1 after delete by another user")
