from typing import Dict
from urllib.request import Request

from django.conf import settings


def settings_context(_request: Request) -> Dict[str, bool]:
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {"DEBUG": settings.DEBUG}
