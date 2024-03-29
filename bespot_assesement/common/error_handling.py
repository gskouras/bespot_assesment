import traceback
from logging import getLogger
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import DatabaseError, IntegrityError
from django.http import Http404
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from bespot_assesement.common.exceptions import ProjectAPIException

logger = getLogger(__name__)


def stringify_exception(exc: Exception) -> List[str]:
    """
    Stringify the exception message.

    :param Exception exc: The exception
    :return: The exception message as a list of one item string.
    :rtype: list(str)
    """
    return [str(exc)]


def stringify_detail_exception(exc: APIException) -> List[str]:
    """
    Stringify the detail attribute of the exception.

    :param rest_framework.exceptions.APIException exc: The exception
    :return: The exception message as a list of one item string.
    :rtype: list(str)
    """
    return [str(exc.detail)]


def stringify_validation_errors(exc: APIException) -> List[str]:
    """
    Stringify the serializer errors.

    :param rest_framework.exceptions.APIException exc: The exception
    :return: The exception messages as a per key list.
    :rtype: list(str)
    """
    error_list = []
    if isinstance(exc.detail, dict):
        for key, value in exc.detail.items():
            error_list.append(f"{key} : {value[0]}")
        return error_list
    else:
        return [str(exc.detail)]


def stringify_django_validation_errors(
    exc: DjangoValidationError,
) -> List[str]:
    """
    Stringify the full_clean errors of model.

    :param DjangoValidationError exc: The exception
    :return: The exception messages as a per key list.
    :rtype: list(str)
    """
    error_list = []
    for key, value in exc.error_dict.items():
        error_list.append(f"{key} : {value[0]}")
    return error_list


def get_exception_handling_dict(exc):
    """
    Populate the exception handling dict with the proper implementation.

    :param Exception exc: The exception
    :return: The dictionary with per exception handling
    :rtype: dict
    """
    try:  # handle case where exception does not have a status code
        code = exc.status_code
    except AttributeError:
        code = HTTP_400_BAD_REQUEST

    if isinstance(exc, ValidationError):
        return {
            "handling_function": stringify_validation_errors,
            "status": HTTP_400_BAD_REQUEST,
        }
    elif isinstance(exc, DjangoValidationError):
        return {
            "handling_function": stringify_django_validation_errors,
            "status": HTTP_400_BAD_REQUEST,
        }
    elif isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return {
            "handling_function": stringify_detail_exception,
            "status": HTTP_401_UNAUTHORIZED,
        }
    elif isinstance(exc, (NotFound, Http404)):
        return {
            "handling_function": stringify_exception,
            "status": HTTP_404_NOT_FOUND,
        }
    elif isinstance(exc, (IntegrityError, DatabaseError)):
        return {
            "handling_function": stringify_exception,
            "status": HTTP_400_BAD_REQUEST,
        }
    elif isinstance(exc, MethodNotAllowed):
        return {
            "handling_function": stringify_detail_exception,
            "status": HTTP_405_METHOD_NOT_ALLOWED,
        }
    elif isinstance(exc, PermissionDenied):
        return {
            "handling_function": stringify_detail_exception,
            "status": HTTP_403_FORBIDDEN,
        }
    elif isinstance(exc, ProjectAPIException):
        return {
            "handling_function": stringify_detail_exception,
            "status": code,
        }
    elif isinstance(exc, APIException):
        return {
            "handling_function": stringify_exception,
            "status": HTTP_400_BAD_REQUEST,
        }
    else:
        return {
            "handling_function": stringify_exception,
            "status": HTTP_500_INTERNAL_SERVER_ERROR,
        }


def error_handler(exc, context):
    """
    The error handler of bespot_assesement API.

    :param Exception exc: The exception being caught
    :param dict context: The context where the exception is being caught
    :return: the Response of the view
    :rtype Response
    """
    try:
        exception_handling_dict = get_exception_handling_dict(exc)
        logger.exception(f"Caught an exception with {context}")
        r = Response(
            {"errors": exception_handling_dict["handling_function"](exc)},
            status=exception_handling_dict["status"],
        )
    except (KeyError, AttributeError, TypeError):
        r = Response(
            {"errors": stringify_exception(exc)},
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        )

        if settings.DEBUG:
            r.data["stacktrace"] = traceback.format_exc()
    return r
