from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


def test_get_v1_account(auth_account_helper):
    with check_status_code_http(expected_status_code=200):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
        GetV1Account.check_response_values(response, login="create_evg_user_56")

def test_get_v1_account_not_auth(account_helper):
    with check_status_code_http(expected_status_code=401, expected_message="User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
