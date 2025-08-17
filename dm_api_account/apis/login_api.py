import requests

from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, json_data: dict, **kwargs):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(path=f'/v1/account/login', json=json_data)
        return response

    # def delete_v1_account_login(self, x_dm_auth_token: str | None, **kwargs):
    #     """
    #     Logout as current user
    #     :param x_dm_auth_token:
    #     :return:
    #     """
    #     headers = {
    #         'X-Dm-Auth-Token': x_dm_auth_token,
    #     }
    #
    #     response = self.delete(path=f'/v1/account/login', headers=headers)
    #     return response

    def delete_v1_account_login(self, **kwargs):
        """
        Logout as current user
        :param kwargs:
        :return:
        """

        response = self.delete(path=f'/v1/account/login')
        return response

    # def delete_v1_account_login_all(self, x_dm_auth_token: str | None, **kwargs):
    #     """
    #     Logout from every device
    #     :param x_dm_auth_token:
    #     :return:
    #     """
    #     headers = {
    #         'X-Dm-Auth-Token': x_dm_auth_token,
    #     }
    #
    #     response = self.delete(path=f'/v1/account/login/all', headers=headers)
    #     return response

    def delete_v1_account_login_all(self, **kwargs):
        """
        Logout from every device
        :param kwargs:
        :return:
        """

        response = self.delete(path=f'/v1/account/login/all')
        return response
