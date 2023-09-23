from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED

from .base import UsersAPITestCase


class TestUsersViewSet(UsersAPITestCase):
    def test_me_no_staff(self) -> None:
        # given
        self.user.is_staff = False
        self.user.save()
        # when
        response = self.client.get(
            path="/api/v1/users/me/",
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        # then
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_me_superuser(self) -> None:
        # given
        self.user.is_staff = True
        self.user.save()
        # when
        response = self.client.get(
            path="/api/v1/users/me/",
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        # then
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_users(self) -> None:
        # given
        self.user.is_staff = True
        self.user.save()
        # when
        response = self.client.get(
            path="/api/v1/users/",
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        # then
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_post_users(self) -> None:
        # given
        self.user.is_staff = True
        self.user.save()
        email = "test@test.com"
        password = "P@ssw0rd!"  # pragma: allowlist secret
        data = {
            "email": email,
            "password": password
        }
        # when
        response = self.client.post(
            path="/api/v1/users/",
            format="json",
            data=data,
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        # then
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json()["email"], email)
