import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login/all")
@allure.sub_suite("Позитивные тесты")
class TestDeleteV1AccountLoginAll:
    @allure.title("Проверка выхода из аккаунта со всех устройств")
    def test_delete_v1_account_login_all(self, auth_account_helper):
        auth_account_helper.dm_account_api.login_api.delete_v1_account_login_all()
