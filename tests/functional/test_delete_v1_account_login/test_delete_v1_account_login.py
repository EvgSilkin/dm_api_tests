import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestDeleteV1AccountLogin:
    @allure.title("Проверка выхода из текущего аккаунта")
    def test_delete_v1_account_login(self, auth_new_account_helper):
        auth_new_account_helper.dm_account_api.login_api.delete_v1_account_login()
