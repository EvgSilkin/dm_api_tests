from datetime import datetime

from hamcrest import assert_that, has_property, starts_with, instance_of, has_properties, equal_to, all_of


class PostV1Account:

    @classmethod
    def check_response_values(cls, response):
        today = datetime.now().strftime("%Y-%m-%d")
        assert_that(str(response.resource.registration), starts_with(today))
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
