from django.test import TestCase
from mock import patch
from pytest import mark

from bespot_assesement.common.tasks  import send_email


@mark.common
@mark.common_tasks
class TestTasks(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestTasks, cls).setUpClass()

    @patch("bespot_assesement.common.tasks.EmailMessage")
    def test_send_email(self, email):
        mail_subject = "Subject"
        message = "This is a message"
        to = ["test@test.com"]
        send_email(mail_subject, message, to)
        email().send.assert_called_once()
