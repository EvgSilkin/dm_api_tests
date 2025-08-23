from datetime import datetime

import pytest
from hamcrest import (assert_that, has_property, has_properties, starts_with, all_of, instance_of,
                      equal_to)
from checkers.http_checkers import check_status_code_http


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    with check_status_code_http(expected_status_code=200):
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, remember_me=True, validate_response=True)
        assert_that(response, all_of(
            has_property("resource", has_property("login", starts_with("activate_evg"))),
            has_property("resource", has_property("registration", instance_of(datetime))),
            has_properties
            ("resource", has_property(
                "rating", has_properties(
                    {
                        "enabled": equal_to(True),
                        "quality": equal_to(0),
                        "quantity": equal_to(0)
                    }
                )))))

@pytest.mark.parametrize(
    "login, email, password, expected_status_code",
    [
        # Успешная регистрация - валидные данные
        (f"ngtv_test_evg_{datetime}", f"evg_{datetime}@example.com", "12345", 400),
        (f"ngtv_test_evg_{datetime}", f"evg_{datetime}example.com", "123456789", 400),
        (f"@", f"evg_{datetime}@example.com", "123456789", 400),
    ]
)
def test_post_v1_account_no_register(account_helper, login, password, email, expected_status_code):
    login = login
    password = password
    email = email

    with check_status_code_http(expected_status_code=400, expected_message="Validation failed"):
        account_helper.register_new_user(login=login, password=password, email=email)

