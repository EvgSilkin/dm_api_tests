from json import loads
from pprint import pprint

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.ligon_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'create_evg_user_12'
    password = '123456789'
    email = f'{login}@mail.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    # Регистрация пользователя
    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь {login} не был создан"

    # Получить активационный токен
    response = mailhog_api.get_api_v2_messages(response)
    print(response.status_code)
    assert response.status_code == 200, f"Письма не были получены {response.json()}"

    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Пользователь {login} не был активирован {response.json()}"

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
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