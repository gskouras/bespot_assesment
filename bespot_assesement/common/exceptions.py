from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class ProjectAPIException(APIException):
    """
    Base class for all custom exceptions inside the application.
    """

    status_code: int = HTTP_400_BAD_REQUEST

    def __init__(self, detail: str, code: int = HTTP_400_BAD_REQUEST):
        """
        Initialize class.

        :param str detail: The detail of the error
        :param int code: The status code
        """
        self.detail = detail
        self.status_code = code
