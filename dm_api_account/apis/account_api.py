import requests


class AccountApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = requests.post(url=f'{self.host}/v1/account', json=json_data)
        return response

    def get_v1_account(self, x_dm_auth_token):
        headers = {
            'X-Dm-Auth-Token': x_dm_auth_token,
        }
        response = requests.get(url=f'{self.host}/v1/account', headers=headers)
        return response

    def put_v1_account_token(self, token):
        """
        Activate registered user
        :param json_data:
        :return:
        """
        response = requests.put(url=f'{self.host}/v1/account/{token}')
        return response

    def post_v1_account_password(self, json_data):
        """
        Reset registered user password
        :param json_data:
        :return:
        """
        response = requests.post('http://5.63.153.31:5051/v1/account/password', json=json_data)
        return response

    def put_v1_account_password(self, json_data):
        """
        Change registered user password
        :param json_data:
        :return:
        """
        response = requests.put(url=f'{self.host}//v1/account/password', json=json_data)
        return response

    def put_v1_account_email(self, json_data):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = requests.put(url=f'{self.host}/v1/account/email', json=json_data)
        return response
