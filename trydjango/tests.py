import os

from django.test import TestCase
from django.contrib.auth.password_validation import validate_password


class PrjConfigTest(TestCase):
    def test_secret_key_strength(self):
        secret_key = os.environ.get('SECRET_KEY')
        try:
            validate_password(secret_key)
        except Exception as ex:
            message = f'{ex.messages}'
            self.fail(message)
