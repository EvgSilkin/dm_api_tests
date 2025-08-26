from datetime import datetime

import allure
import pytest
from hamcrest import (assert_that, has_property, has_properties, starts_with, all_of, instance_of,
                      equal_to)
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


@allure.suite("Тесты на проверку метода POST v1/account")
@allure.sub_suite("Позитивные тесты")
class TestPostV1Account:
    def test_post_v1_account(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with check_status_code_http(expected_status_code=200):
            account_helper.register_new_user(login=login, password=password, email=email)
            response = account_helper.user_login(login=login, password=password, remember_me=True,
                                                 validate_response=True)
            PostV1Account.check_response_values(response)
