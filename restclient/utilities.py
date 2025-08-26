import allure
import json
import curlify


def allure_attach(fn):
    """
    Декоратор для прикрепления информации о запросе и ответе в Allure отчет.
    Attaches request body, curl command, and response body to Allure report.
    """

    def wrapper(*args, **kwargs):
        # Прикрепляем тело запроса
        body = kwargs.get("json")
        if body:
            allure.attach(
                json.dumps(body, indent=4),
                name="request_body",
                attachment_type=allure.attachment_type.JSON,
            )

        # Выполняем запрос
        response = fn(*args, **kwargs)

        # Прикрепляем curl команду
        curl = curlify.to_curl(response.request)
        allure.attach(curl, name="curl", attachment_type=allure.attachment_type.TEXT)

        # Обрабатываем ответ
        try:
            # Получаем JSON данные, но не перезаписываем response.json
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            # Если ответ не в JSON формате
            response_text = response.text
            status_code = f"status code = {response.status_code}"
            allure.attach(
                response_text if len(response_text) > 0 else status_code,
                name="response.body",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            # Если ответ в JSON формате
            allure.attach(
                json.dumps(response_json, indent=4),
                name="response.body",
                attachment_type=allure.attachment_type.JSON,
            )

        return response

    return wrapper