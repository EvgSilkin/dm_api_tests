import structlog

from helpers.account_helper import AccountHelper
from restclient.configuratiton import Configuration as DmApiConfiguration
from restclient.configuratiton import Configuration as MailhogConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)


def test_put_v1_account_token():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025', disable_log=True)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'activate_evg_user_22'
    password = '123456789'
    email = f'{login}@mail.com'

    account_helper.register_new_user(login=login, password=password, email=email)
