# from rest_framework.views import exception_handler
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class BaseException(Exception):
    def __init__(self, message, error_code="bm_error") -> None:
        super().__init__(message, error_code)
        self.message = message
        self.error_code = error_code


def _get_error_details(data, default_code=None):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings or strings into `ErrorDetail`.
    """
    if isinstance(data, (list, tuple)):
        ret = [_get_error_details(item, default_code) for item in data]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {key: _get_error_details(value, default_code) for key, value in data.items()}
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    text = force_str(data)
    code = getattr(data, "code", default_code)
    return ErrorDetail(text, code)


class BaseAPIException(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("A server error occurred.")
    default_code = "error"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        self.detail = _get_error_details(detail, code)


""" def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response
    response = exception_handler(exc, context)

    # If a response exists, modify it to include the custom code
    if response is not None:
        if isinstance(response.data, dict) and "detail" in response.data:
            # Add a custom code (you can map the codes to specific exceptions)
            response.data["code"] = (
                "no-active-account"  # You can change this based on the error
            )

    return response
 """
