from logging import getLogger
from typing import Any

from django.contrib.auth.models import User
from django.core.management import BaseCommand

logger = getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Run the command.

        :param list(str) args: The list of args
        :param dict options: The list of kwargs
        """
        logger.debug(f"N users is {User.objects.count()}")
