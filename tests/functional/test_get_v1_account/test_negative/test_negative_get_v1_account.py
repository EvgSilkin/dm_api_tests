import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


@allure.suite("Тесты на проверку метода GET v1/account")
@allure.sub_suite("Негативные тесты")
class TestNegativeGetV1Account:

    @allure.title("Проверка получения пользователя без авторизации")
    def test_get_v1_account_not_auth(self, account_helper):
        with check_status_code_http(expected_status_code=401, expected_message="User must be authenticated"):
            account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
