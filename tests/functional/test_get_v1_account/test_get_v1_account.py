from hamcrest import assert_that, has_property, equal_to, starts_with, all_of, not_none, has_properties
from checkers.http_checkers import check_status_code_http


def test_get_v1_account(auth_account_helper):
    with check_status_code_http(expected_status_code=200):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
        assert_that(response, all_of(
            has_property("resource", has_property("login", starts_with("create_evg_user"))),
            has_property("resource", has_property("info", equal_to(""))),
            has_property("resource", has_property("online", not_none())),
            has_property("resource", has_property("rating", has_properties(
                {
                    "enabled": equal_to(True),
                    "quality": equal_to(0),
                    "quantity": equal_to(0)
                }
            ))),
            has_property("resource", has_property("registration", not_none())),
            has_property("resource", has_property("roles", equal_to(
                [
                    "Guest",
                    "Player"
                ]
            ))
                         ),
            has_property("resource", has_property("settings", has_property("color_schema",
                                                                           equal_to("Modern")))),
            has_property("resource", has_property("settings", has_property("paging", has_properties(
                {
                    "comments_per_page": equal_to(10),
                    "entities_per_page": equal_to(10),
                    "messages_per_page": equal_to(10),
                    "posts_per_page": equal_to(10),
                    "topics_per_page": equal_to(10)
                }
            )))),

        ))

def test_get_v1_account_not_auth(account_helper):
    with check_status_code_http(expected_status_code=401, expected_message="User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
