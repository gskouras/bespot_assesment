# from django.test import TestCase
# from mock import patch
# from pytest import mark

# from bespot_assesement.places.tasks import get_users_count

# @mark.users
# @mark.users_tasks
# class TestTasks(TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         super(TestTasks, cls).setUpClass()

#     @patch("bespot_assesement.places.tasks.User")
#     def test_get_users_count(self, user):
#         user.objects.count.return_value = 1
#         return_value = get_users_count()
#         self.assertEqual(1, return_value)
