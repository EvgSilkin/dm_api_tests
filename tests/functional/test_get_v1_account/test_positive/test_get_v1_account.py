import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


@allure.suite("Тесты на проверку метода GET v1/account")
@allure.sub_suite("Позитивные тесты")
class TestGetV1Account:
    @allure.title("Проверка получения пользователя после авторизации")
    def test_get_v1_account(self, auth_account_helper):
        with check_status_code_http(expected_status_code=200):
            response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
            print(response)
            GetV1Account.check_response_values(response, login="create_evg_user_56")
