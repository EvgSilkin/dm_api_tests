import requests


class LoginApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account_login(self, json_data: dict, **kwargs):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = requests.post(url=f'{self.host}/v1/account/login', json=json_data)
        return response

    def delete_v1_account_login(self, x_dm_auth_token: str | None, **kwargs):
        """
        Logout as current user
        :param x_dm_auth_token:
        :return:
        """
        headers = {
            'X-Dm-Auth-Token': x_dm_auth_token,
        }

        response = requests.delete(url=f'{self.host}/v1/account/login', headers=headers)
        return response

    def delete_v1_account_login_all(self, x_dm_auth_token: str | None, **kwargs):
        """
        Logout from every device
        :param x_dm_auth_token:
        :return:
        """
        headers = {
            'X-Dm-Auth-Token': x_dm_auth_token,
        }

        response = requests.delete(url=f'{self.host}/v1/account/login/all', headers=headers)
        return response

