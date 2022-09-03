from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('khl', password='abc123')
