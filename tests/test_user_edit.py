import allure
from datetime import datetime
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Check edit cases")
class TestUserEdit(BaseCase):

    @allure.description("This test edit of created user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("positive_case")
    def test_edit_just_created_user(self):
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

        # Edit
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers = {"x-csrf-token":token},
            cookies = {"auth_sid": auth_sid},
            data = {"firstName":new_name})

        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    @allure.description("This test edit of non-authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("negative_case")
    def test_edit_non_authorized_user(self):
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

        # Edit
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name})
        Assertions.assert_code_status(response3, 400)

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(response4, "firstName", first_name,
                                             "Wrong name of the user after edit without authorization")

    @allure.description("This test edit by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("negative_case")
    def test_edit_user_by_another_user(self):
        # Register user1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email1 = register_data1['email']
        first_name1 = register_data1['firstName']
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

        # Edit
        new_name = "Changed Name"
        response5 = MyRequests.put(f"/user/{user_id1}",
                                 headers={'x-csrf-token': token2},
                                 cookies={'auth_sid': auth_sid2},
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response5, 200)

        # Get user1
        response6 = MyRequests.get(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
        )
        Assertions.assert_json_value_by_name(response6, "firstName", first_name1,
                                             "Wrong name of the user 1 after edit by another user")

    @allure.description("This test edit of email by incorrect value")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("negative_case")
    def test_edit_email_by_incorrect_value(self):
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

        # Edit
        new_email = datetime.now().strftime("%m%d%Y%H%M%S")
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email})

        Assertions.assert_code_status(response3, 400)
        assert response3.text == 'Invalid email format', "Unexpected response text for invalid email"

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(response4, "email", email,
                                             "Wrong email after edit")

    @allure.description("This test edit of name by incorrect short value")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("negative_case")
    def test_edit_firstName_by_short_value(self):
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

        # Edit
        new_firstName = 'a'
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstName})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Too short value for field firstName",
                                             "Unexpected value for short name")

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(response4, "firstName", first_name,
                                             "Wrong email after edit")