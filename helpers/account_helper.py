from json import loads
from requests import Response

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


class AccountHelper:

    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь {login} не был создан"

        token = self.get_activate_token_by_login(response=response, login=login)
        response = self.activate_user(login=login, token=token)

        return response

    def user_login(self, login: str, password: str, remember_me: bool = True, expected_status_code: int = 200):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == expected_status_code, \
            (f"Статус код {response.status_code} при авторизации пользователя {login} не соответствует "
             f"ожидаемому {expected_status_code}:"
             f" {response.json()}")
        return response

    def change_user_email(self, login: str, password: str, new_mailbox: str, email_domain: str):
        json_data = {
            "login": login,
            "password": password,
            "email": f'{new_mailbox}@{email_domain}'
        }

        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f"Для пользователя {login} не был обновлен email {response.json()}"
        return response

    def get_activate_token_by_login(self, response: Response, login: str):
        response = self.mailhog.mailhog_api.get_api_v2_messages(response)
        assert response.status_code == 200, f"Письма не были получены {response.json()}"

        token = self._get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        return token

    def get_activate_token_by_mailbox(self, login: str, new_mailbox: str):
        
        assert response.status_code == 200, f"Письма не были получены {response.json()}"

        token = self._get_activation_token_by_mailbox(new_mailbox=new_mailbox, response=response)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        return token

    def activate_user(self, login: str, token: str):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Пользователь {login} не был активирован {response.json()}"
        return response

    @staticmethod
    def _get_activation_token_by_login(login, response):
        token = None

        for item in response.json().get('items'):
            user_data = loads(item.get('Content').get('Body'))
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data.get('ConfirmationLinkUrl').split('/')[-1]
        return token

    @staticmethod
    def _get_activation_token_by_mailbox(new_mailbox, response):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_mailbox = item['To'][0]['Mailbox']
            if user_mailbox == new_mailbox:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token
