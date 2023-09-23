from django.core.management import call_command
from django.test import TransactionTestCase


class TestCommand(TransactionTestCase):
    def test_handle(self) -> None:
        call_command("count_users")
