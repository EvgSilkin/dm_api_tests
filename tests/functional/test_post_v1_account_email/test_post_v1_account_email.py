from json import loads
from pprint import pprint

import structlog

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuratiton import Configuration as AccountApiConfiguration
from restclient.configuratiton import Configuration as LoginApiConfiguration
from restclient.configuratiton import Configuration as MailhogConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

def test_post_v1_account_email():
    account_api_configuration = AccountApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    login_api_configuration = LoginApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')

    account_api = AccountApi(configuration=account_api_configuration)
    login_api = LoginApi(configuration=login_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    login = 'ch_mail_evg_user_17'
    password = '123456789'
    email = f'{login}@mail.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    # Регистрация пользователя
    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь {login} не был создан"

    # Получение активационного токена
    response = mailhog_api.get_api_v2_messages(response)
    assert response.status_code == 200, f"Письма не были получены {response.json()}"

    token = get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"Пользователь {login} не был активирован {response.json()}"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f"Пользователь {login} не был авторизован {response.json()}"

    # Измениние email
    new_mailbox = "new_mail_evg_17"
    json_data = {
        "login": login,
        "password": password,
        "email": f'{new_mailbox}@mail.com'
    }

    response = account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, f"Для пользователя {login} не был обновлен email {response.json()}"

    # Получение 403 при авторизации
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, f"Пользователь {login} не получил ошибку 403 {response.json()}"

    # Получение нового активационного токена
    response = mailhog_api.get_api_v2_messages(response)
    assert response.status_code == 200, f"Письма не были получены {response.json()}"

    token = get_activation_token_by_mailbox(new_mailbox=new_mailbox, response=response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя по новому email
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"Пользователь {login} не был активирован {response.json()}"

    # Авторизация с новым email
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f"Пользователь {login} не был авторизован {response.json()}"


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json().get('items'):
        user_data = loads(item.get('Content').get('Body'))
        pprint(user_data)
        user_login = user_data.get('Login')
        pprint(user_login)
        if user_login == login:
            pprint(user_data.get('ConfirmationLinkUrl'))
            token = user_data.get('ConfirmationLinkUrl').split('/')[-1]
    return token


def get_activation_token_by_mailbox(new_mailbox, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_mailbox = item['To'][0]['Mailbox']
        if user_mailbox == new_mailbox:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
