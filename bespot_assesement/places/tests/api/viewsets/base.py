from typing import Callable, Dict, Any

from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APITestCase

from bespot_assesement.places.tests.factories import UserFactory


class UsersAPITestCase(APITestCase):
    def setUp(self) -> None:
        super(UsersAPITestCase, self).setUp()
        self.email = "user@user.com"
        self.password = "P@ssw0rd!"  # pragma: allowlist secret
        self.user = UserFactory(is_active=True, username=self.email,
                                email=self.email,
                                password=make_password(self.password))
        self.token = Token.objects.get_or_create(user=self.user)[0].key

    def perform_request(
        self,
        method: Callable,
        url: str,
        data: Dict[str, Any] = None,
    ) -> Response:
        """
        Perform an actual request in Portal API based on specific parameters.

        :param Callable method: The HTTP method that the client will perform
        :param str url: The endpoint of the request
        :param dict data: The data of the request in case the method is POST.

        :return: The response of the Request
        :rtype: requests.Response
        :param token: User's Token
        """

        token = data["token"] if "token" in data else self.token

        return method(
            path=url,
            data=data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )
