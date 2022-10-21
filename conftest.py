import datetime
import pytest
import django

# from jose import jwt
from django.conf import settings
from rest_framework.test import APIClient as Client


def pytest_configure():
    # config vars
    settings.PROJECT = "smenu-core"

    # config database
    # TODO ??
    django.setup()


@pytest.fixture
def client():
    def factory(uid=None, roles=None):
        return Client()
        if not uid:
            return Client()

        client = Client()
        # client.credentials(HTTP_AUTHORIZATION=settings.AUTH_PREFIX + " " + token)
        return client

    return factory