from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.ligon_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account_email():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'ch_mail_evg_user_09'
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

    # Получение активационного токена
    response = mailhog_api.get_api_v2_messages(response)
    print(response.status_code)
    assert response.status_code == 200, f"Письма не были получены {response.json()}"

    token = get_activation_token_by_login(login=login, response=response)
    print(token)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Пользователь {login} не был активирован {response.json()}"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Пользователь {login} не был авторизован {response.json()}"

    # Измениние email
    new_mailbox = "new_mail_evg_09"
    json_data = {
        "login": login,
        "password": password,
        "email": f'{new_mailbox}@mail.com'
    }

    response = account_api.put_v1_account_email(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Для пользователя {login} не был обновлен email {response.json()}"

    # Получение 403 при авторизации
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, f"Пользователь {login} не получил ошибку 403 {response.json()}"

    # Получение нового активационного токена
    response = mailhog_api.get_api_v2_messages(response)
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200, f"Письма не были получены {response.json()}"

    token = get_activation_token_by_mailbox(new_mailbox=new_mailbox, response=response)
    print(token)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя по новому email
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Пользователь {login} не был активирован {response.json()}"

    # Авторизация с новым email
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
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token


def get_activation_token_by_mailbox(new_mailbox, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_mailbox = item['To'][0]['Mailbox']
        if user_mailbox == new_mailbox:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
