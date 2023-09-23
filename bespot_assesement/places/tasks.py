from django.contrib.auth.models import User

from config import celery_app


@celery_app.task()
def get_users_count() -> int:
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()
