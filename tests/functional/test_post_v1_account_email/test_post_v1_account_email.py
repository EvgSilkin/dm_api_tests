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


def test_post_v1_account_email():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025', disable_log=True)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'ch_mail_evg_user_27'
    password = '123456789'
    email = f'{login}@mail.com'

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password, remember_me=True)

    new_mailbox = "new_mail_evg_27"
    account_helper.change_user_email(login=login, password=password, new_mailbox=new_mailbox, email_domain="mail.ru")

    # Получение 403 при авторизации
    response = account_helper.user_login(login=login, password=password, remember_me=True, expected_status_code=403)

    token = account_helper.get_activation_token_by_mailbox(new_mailbox=new_mailbox)
    account_helper.activate_user(login=login, token=token)
    account_helper.user_login(login=login, password=password, remember_me=True)



