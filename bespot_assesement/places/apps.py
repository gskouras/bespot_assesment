from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bespot_assesement.places"
    verbose_name = _("Users")

    def ready(self) -> None:
        try:
            import bespot_assesement.places.signals  # noqa F401 # pylint: disable=unused-import
        except ImportError:
            pass
