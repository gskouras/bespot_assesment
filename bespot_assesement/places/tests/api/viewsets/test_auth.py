from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .base import UsersAPITestCase

class TestAuthViewSet(UsersAPITestCase):
    def test_login_happy_path(self) -> None:
        # given
        data = {
            "email": self.email,
            "password": self.password,  # pragma: allowlist secret
        }

        # when
        response = self.client.post(
            path="/api/v1/auth/sign-in/",
            data=data,
            format="json",
        )
        # then
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_login_error(self) -> None:
        # given
        data = {
            "email": self.email,
            "password": "error",  # pragma: allowlist secret
        }

        # when
        response = self.client.post(
            path="/api/v1/auth/sign-in/",
            data=data,
            format="json",
        )
        # then
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
