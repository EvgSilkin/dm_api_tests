import uuid
from pprint import pprint

import structlog
import curlify
from requests import session, JSONDecodeError

from restclient.configuratiton import Configuration
from restclient.utilities import allure_attach


class RestClient:

    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.set_headers(configuration.headers)
        self.disable_log = configuration.disable_log
        self.session = session()
        # Инициализация лога
        self.log = structlog.get_logger(__name__).bind(service='api')

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def get(self, path, **kwargs):
        return self._send_request(method='GET', path=path, **kwargs)

    def post(self, path, **kwargs):
        return self._send_request(method='POST', path=path, **kwargs)

    def put(self, path, **kwargs):
        return self._send_request(method='PUT', path=path, **kwargs)

    def patch(self, path, **kwargs):
        return self._send_request(method='PATCH', path=path, **kwargs)

    def delete(self, path, **kwargs):
        return self._send_request(method='DELETE', path=path, **kwargs)

    @allure_attach
    def _send_request(self, method: str, path: str, **kwargs):
        # Забиндить уникальный uuid для каждого лога
        log = self.log.bind(event_id=str(uuid.uuid4()))

        full_url = self.host + path

        if self.disable_log:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            return rest_response

        # Вывод лога запроса
        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data'),
        )

        # Выполнить запрос
        rest_response = self.session.request(method=method, url=full_url, **kwargs)
        curl = curlify.to_curl(rest_response.request)
        pprint(curl)
        # Вывод лога ответа
        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            header=rest_response.headers,
            json=self._get_json(rest_response)
        )
        rest_response.raise_for_status()
        return rest_response

    # Проверить наличие json в ответе, иначе возвращать {}
    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
