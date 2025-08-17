import time
from json import loads
from pprint import pprint

from requests import Response

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retrier(retry_count: int, retry_delay: int):
    def decorator(function):
        def wrapper(*args, **kwargs):
            token = None
            current_count = 0
            while token is None:
                if current_count == retry_count:
                    raise AssertionError("Превышено максимальное количество попыток запроса")
                token = function(*args, **kwargs)
                if token is not None:
                    return token
                current_count += 1
                time.sleep(retry_delay)
            return token

        return wrapper

    return decorator


class AccountHelper:

    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login: str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={
                "login": login,
                "password": password
            })
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь {login} не был создан"

        token = self.get_activation_token_by_login(login=login)
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

    def activate_user(self, login: str, token: str):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Пользователь {login} не был активирован {response.json()}"
        return response

    @retrier(retry_count=5, retry_delay=1)
    def get_activation_token_by_login(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f"Письма не были получены {response.json()}"
        for item in response.json().get('items'):
            user_data = loads(item.get('Content').get('Body'))
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data.get('ConfirmationLinkUrl').split('/')[-1]
                assert token is not None, f"Токен для пользователя {login} не был получен"
        return token

    @retrier(retry_count=5, retry_delay=1)
    def get_activation_token_by_mailbox(self, new_mailbox):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f"Письма не были получены {response.json()}"
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_mailbox = item['To'][0]['Mailbox']
            if user_mailbox == new_mailbox:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                assert token is not None, f"Токен для mailbox {new_mailbox} не был получен"
        return token

    @retrier(retry_count=5, retry_delay=1)
    def get_reset_password_token_by_login(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f"Письма не были получены {response.json()}"
        for item in response.json().get('items'):
            user_data = loads(item.get('Content').get('Body'))
            user_login = user_data.get('Login')
            if user_login == login and user_data.get("ConfirmationLinkUri"):
                token = user_data.get('ConfirmationLinkUri').split('/')[-1]
                assert token is not None, f"Токен для изменение пароля пользователя {login} не был получен"

        return token

    def change_password(self, login: str, old_password: str, new_password: str):
        self.auth_client(login=login, password=old_password)

        json_data = {
            "login": login,
            "email": f"{login}@mail.com"
        }
        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code == 200, (f"Запрос для изменение пароля пользователя не был отправлен"
                                             f" {response.json()}")
        reset_password_token = self.get_reset_password_token_by_login(login=login)
        json_data = {
            "login": login,
            "token": reset_password_token,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)
        assert response.status_code == 200, (f"Пароль не был обновлен {response.json()}")
        response = self.user_login(login=login, password=new_password)
        return response





