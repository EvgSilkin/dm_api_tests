from dm_api_account.models.request_models.change_email import ChangeEmail
from dm_api_account.models.request_models.change_password import ChangePassword
from dm_api_account.models.request_models.registration import Registration
from dm_api_account.models.request_models.reset_password import ResetPassword
from dm_api_account.models.response_models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.response_models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration, **kwargs):
        """
        Register new user
        :return:
        """
        response = self.post(path=f'/v1/account', json=registration.model_dump(exclude_none=True, by_alias=True))
        # exclude_none=True - если поля необязательно и не заполнено, то его не передавать
        return response

    def get_v1_account(self, **kwargs):
        """
        Get current user
        :param kwargs:
        :return:
        """
        response = self.get(path=f'/v1/account', **kwargs)
        print(response.json())
        UserDetailsEnvelope(**response.json())
        return response

    def put_v1_account_token(self, token: str | None, validate_response=True, **kwargs):
        """
        Activate registered user
        :param validate_response:
        :param token:
        :param kwargs:
        :return:
        """
        response = self.put(path=f'/v1/account/{token}')
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def post_v1_account_password(self, reset_password: ResetPassword, validate_response=True, **kwargs):
        """
        Reset registered user password
        :param reset_password:
        :param validate_response:
        :param kwargs:
        :return:
        """
        response = self.post(path='/v1/account/password', json=reset_password.model_dump(exclude_none=True,
                                                                                         by_alias=True))

        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_password(self, change_password: ChangePassword, validate_response=True, **kwargs):
        """
        Change registered user password
        :param validate_response:
        :param change_password:
        :return:
        """
        response = self.put(path=f'/v1/account/password', json=change_password.model_dump(exclude_none=True,
                                                                                          by_alias=True))
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_email(self, change_email: ChangeEmail, validate_response=True, **kwargs):
        """
        Change registered user email
        :param validate_response:
        :param change_email:
        :return:
        """
        response = self.put(path=f'/v1/account/email', json=change_email.model_dump(exclude_none=True, by_alias=True))
        if validate_response:
            return UserEnvelope(**response.json())
        return response
