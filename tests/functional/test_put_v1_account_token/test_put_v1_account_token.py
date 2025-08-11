from json import loads
from pprint import pprint

import structlog

from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuratiton import Configuration as AccountApiConfiguration
from restclient.configuratiton import Configuration as MailhogConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)


def test_put_v1_account_token():
    account_api_configuration = AccountApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')

    account_api = AccountApi(configuration=account_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    login = 'activate_evg_user_14'
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

    # Получить активационный токен
    response = mailhog_api.get_api_v2_messages(response)
    assert response.status_code == 200, f"Письма не были получены {response.json()}"

    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"Пользователь {login} не был активирован {response.json()}"


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
