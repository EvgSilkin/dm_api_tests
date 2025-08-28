from datetime import datetime

import allure
import assertpy
import hamcrest
from hamcrest import has_property, starts_with, equal_to, not_none, has_properties, all_of
from assertpy import soft_assertions

from clients.http.dm_api_account.models.response_models.user_details_envelope import UserRole


class GetV1Account:

    @classmethod
    def check_response_values(cls, response, login):
        with allure.step("Проверка ответа запроса GET /v1/account"):
            hamcrest.assert_that(response, all_of(
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
            with soft_assertions():
                assertpy.assert_that(response.resource.login).is_equal_to(login)
                assertpy.assert_that(response.resource.online).is_instance_of(datetime)
                assertpy.assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
