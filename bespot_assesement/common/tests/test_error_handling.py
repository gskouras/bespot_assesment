from unittest import TestCase

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import DatabaseError, IntegrityError
from django.http import Http404
from mock import MagicMock, patch
from pytest import mark
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from bespot_assesement.common.error_handling import (
    error_handler,
    get_exception_handling_dict,
    stringify_detail_exception,
    stringify_django_validation_errors,
    stringify_exception,
    stringify_validation_errors,
)
from bespot_assesement.common.exceptions import ProjectAPIException


@mark.common
@mark.common_exceptions
class TestException(TestCase):
    def test_stringify_exception(self):
        error_message = "This is a message"
        exception = Exception(error_message)

        output = stringify_exception(exception)

        self.assertEqual(output, [error_message])

    def test_stringify_detail_exception(self):
        error_message = "This is a message"
        exception = APIException()
        exception.detail = error_message

        output = stringify_detail_exception(exception)

        self.assertEqual(output, [error_message])

    def test_stringify_validation_errors(self):
        exception = APIException()
        exception.detail = {
            "key_1": ("Issue 1", 200),
            "key_2": ("Issue 2", 200),
        }

        output = stringify_validation_errors(exception)

        self.assertEqual(
            output,
            [
                "key_1 : Issue 1",
                "key_2 : Issue 2",
            ],
        )

    def test_stringify_validation_errors_attribute_error(self):
        exception = APIException()
        exception.detail = [
            {"key_1": ("Issue 1", 200)},
            {"key_2": ("Issue 2", 200)},
        ]

        output = stringify_validation_errors(exception)

        self.assertEqual(
            output,
            ["[{'key_1': ('Issue 1', 200)}, {'key_2': ('Issue 2', 200)}]"],
        )

    def test_stringify_django_validation_errors(self):
        exception = DjangoValidationError(message="")
        exception.error_dict = {
            "key_1": ("Issue 1", 200),
            "key_2": ("Issue 2", 200),
        }

        output = stringify_django_validation_errors(exception)

        self.assertEqual(
            output,
            [
                "key_1 : Issue 1",
                "key_2 : Issue 2",
            ],
        )

    def test_get_exception_handling_dict_django_validation_error(self):
        exception = DjangoValidationError("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_django_validation_errors,
                "status": HTTP_400_BAD_REQUEST,
            },
        )

    def test_get_exception_handling_dict_validation_error(self):
        exception = ValidationError("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_validation_errors,
                "status": HTTP_400_BAD_REQUEST,
            },
        )

    def test_get_exception_handling_dict_not_auth_error(self):
        exception = NotAuthenticated("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_detail_exception,
                "status": HTTP_401_UNAUTHORIZED,
            },
        )

    def test_get_exception_handling_dict_auth_failed_error(self):
        exception = AuthenticationFailed("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_detail_exception,
                "status": HTTP_401_UNAUTHORIZED,
            },
        )

    def test_get_exception_handling_dict_not_found_error(self):
        exception = NotFound("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_exception,
                "status": HTTP_404_NOT_FOUND,
            },
        )

    def test_get_exception_handling_dict_404_error(self):
        exception = Http404("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_exception,
                "status": HTTP_404_NOT_FOUND,
            },
        )

    def test_get_exception_handling_integrity_error(self):
        exception = IntegrityError("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_exception,
                "status": HTTP_400_BAD_REQUEST,
            },
        )

    def test_get_exception_handling_dict_not_allowed_error(self):
        exception = MethodNotAllowed("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_detail_exception,
                "status": HTTP_405_METHOD_NOT_ALLOWED,
            },
        )

    def test_get_exception_handling_dict_permission_denied_error(self):
        exception = PermissionDenied("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_detail_exception,
                "status": HTTP_403_FORBIDDEN,
            },
        )

    def test_get_exception_handling_dict_project_error(self):
        exception = ProjectAPIException("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_detail_exception,
                "status": HTTP_400_BAD_REQUEST,
            },
        )

    def test_get_exception_handling_dict_api_error(self):
        exception = APIException("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_exception,
                "status": HTTP_400_BAD_REQUEST,
            },
        )

    def test_get_exception_handling_database_error(self):
        exception = DatabaseError("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_exception,
                "status": HTTP_400_BAD_REQUEST,
            },
        )

    def test_get_exception_handling_unknown_error(self):
        class TestException(Exception):
            pass

        exception = TestException("Error")

        output = get_exception_handling_dict(exception)

        self.assertEqual(
            output,
            {
                "handling_function": stringify_exception,
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
            },
        )

    @patch("bespot_assesement.common.error_handling.settings")
    @patch(
        "bespot_assesement.common.error_handling."
        "get_exception_handling_dict"
    )
    def test_error_handler_handled_exception(self, get_dict, settings):
        exception = Exception("test")
        context = MagicMock()
        settings.DEBUG = True
        get_dict.return_value = {
            "handling_function": stringify_exception,
            "status": HTTP_400_BAD_REQUEST,
        }

        error_handler(exception, context)

    @patch("bespot_assesement.common.error_handling.settings")
    @patch(
        "bespot_assesement.common.error_handling."
        "get_exception_handling_dict"
    )
    def test_error_handler_unhandled_exception(self, get_dict, settings):
        exception = Exception("test")
        context = MagicMock()
        settings.DEBUG = True
        get_dict.side_effect = AttributeError("Error")
        error_handler(exception, context)
