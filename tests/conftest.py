from collections import namedtuple
from datetime import datetime
from pathlib import Path

import pytest
import structlog

from helpers.account_helper import AccountHelper
from restclient.configuratiton import Configuration as DmApiConfiguration
from restclient.configuratiton import Configuration as MailhogConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from vyper import v

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"), disable_log=True)
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture(scope="session")
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)

    account_helper.auth_client(login=v.get("user.login"), password=v.get("user.password"))
    return account_helper


@pytest.fixture(scope="module")
def auth_new_account_helper(mailhog_api, prepare_user_scope_session):
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)

    login = prepare_user_scope_session.login
    password = prepare_user_scope_session.password
    email = prepare_user_scope_session.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.auth_client(login=login, password=password)
    return account_helper


# @pytest.fixture(scope="session")
# def auth_account_helper(mailhog_api):
#     def _get_login_and_password(login: str, password: str):
#         dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
#         account = DMApiAccount(configuration=dm_api_configuration)
#         account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
#
#         account_helper.auth_client(login=login, password=password)
#         return account_helper
#     return _get_login_and_password


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'activate_evg_{data}'
    password = v.get("user.password")
    email = f'{login}@mail.com'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user


@pytest.fixture(scope="session")
def prepare_user_scope_session():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'activate_evg_{data}'
    password = v.get("user.password")
    email = f'{login}@mail.com'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
