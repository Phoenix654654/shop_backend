from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 404:
            response.data = {
                "detail": "К сожалению, запрашиваемый объект не найден!",
                "status": 404,
            }

        elif isinstance(exc, ValidationError):
            errors = set()
            non_field_key = api_settings.NON_FIELD_ERRORS_KEY

            def parse_errors(data, prefix=""):
                if isinstance(data, dict):
                    for field, messages in data.items():
                        if field in (non_field_key, "detail"):
                            parse_errors(messages, prefix)
                        else:
                            parse_errors(messages, f"{prefix}{field} - ")
                elif isinstance(data, list):
                    for msg in data:
                        parse_errors(msg, prefix)
                else:
                    errors.add(f"{prefix}{data}")

            parse_errors(response.data)

            response.data = {
                "detail": "; ".join(errors),
                "status": 400,
            }

        else:
            response.data = {
                "detail": response.data.get("detail", "Произошла ошибка"),
                "status": response.status_code,
            }

    return response
