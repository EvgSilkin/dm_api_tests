from datetime import datetime

import allure
import pytest
from hamcrest import (assert_that, has_property, has_properties, starts_with, all_of, instance_of,
                      equal_to)
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


@allure.suite("Тесты на проверку метода POST v1/account")
@allure.sub_suite("Негативные тесты")
class TestNegativePostV1Account:
    @pytest.mark.parametrize(
        "login, email, password, expected_status_code",
        [
            # Успешная регистрация - валидные данные
            (f"ngtv_test_evg_{datetime.now()}", f"evg_{datetime.now()}@example.com", "12345", 400),
            (f"ngtv_test_evg_{datetime.now()}", f"evg_{datetime.now()}example.com", "123456789", 400),
            (f"@", f"evg_{datetime.now()}@example.com", "123456789", 400),
        ]
    )
    @allure.title("Проверка выхода из аккаунта со всех устройств")
    def test_post_v1_account_no_register(self, account_helper, login, password, email, expected_status_code):
        login = login
        password = password
        email = email

        with check_status_code_http(expected_status_code=400, expected_message="Validation failed"):
            account_helper.register_new_user(login=login, password=password, email=email)
