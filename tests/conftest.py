import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path

import pytest
import structlog
from vyper import v
from swagger_coverage_py.reporter import CoverageReporter

from helpers.account_helper import AccountHelper
from packages.restclient.configuratiton import Configuration as DmApiConfiguration
from packages.restclient.configuratiton import Configuration as MailhogConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

options = (
    "service.dm_api_account",
    "service.mailhog",
    "user.login",
    "user.password",
    "telegram.chat_id",
    "telegram.token"
)
# http://5.63.153.31:5051/swagger/Account/swagger.json?urls.primaryName=Account

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://5.63.153.31:5051")
    reporter.setup("/swagger/Account/swagger.json")

    yield
    reporter.generate_report()
    reporter.cleanup_input_files()


@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    config_dir = Path(__file__).parent.parent / "config"
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config_dir)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))
    os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get("telegram.chat_id")
    os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get("telegram.token")


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stg", help="run stg")

    for option in options:
        parser.addoption(f"--{option}", action="store")


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"), disable_log=False)
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
    password = '123456789'
    email = f'{login}@mail.com'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user


@pytest.fixture(scope="session")
def prepare_user_scope_session():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'activate_evg_{data}'
    password = '123456789'
    email = f'{login}@mail.com'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
