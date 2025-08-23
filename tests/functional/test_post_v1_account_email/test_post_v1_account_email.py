def test_post_v1_account_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password, remember_me=True)

    new_mailbox = f"new_{login}"
    account_helper.change_user_email(login=login, password=password, new_mailbox=new_mailbox, email_domain="mail.ru")

    # Получение 403 при авторизации
    account_helper.user_login(login=login, password=password, remember_me=True, expected_status_code=403)

    token = account_helper.get_activation_token_by_mailbox(new_mailbox=new_mailbox)
    account_helper.activate_user(login=login, token=token)
    account_helper.user_login(login=login, password=password, remember_me=True)
