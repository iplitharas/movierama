import os

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from movies.models import Movie

DEFAULT_ENGINE = "django.db.backends.sqlite3"

from typing import Any, Tuple


@pytest.fixture()
def fake_user_with_one_movie() -> Tuple[Movie, Any]:
    User = get_user_model()
    default_password = "password123"
    user = User(username="bob")
    user.set_password(default_password)
    user.save()
    movie = Movie.objects.create(
        author=user,
        title="Harry Potter and the Deathly Hallows: Part 2",
        desc="A clash between good and evil awaits as young Harry (Daniel Radcliffe)",
        genre="Fantasy",
        year="2011",
    )
    return user, movie


# @pytest.fixture(scope="session")
# def django_db_settings(django_db_setup):
#     settings.DATABASES["default"] = {
#         "ENGINE": os.environ.get("DB_TEST_ENGINE", DEFAULT_ENGINE),
#         "USER": os.environ.get("DB_TEST_USER", "user"),
#         "PASSWORD": os.environ.get("DB_TEST_PASSWORD", "password"),
#         "NAME": os.environ.get("DB_TEST_NAME", "DB_TEST"),
#         "PORT": os.environ.get("DB_TEST_PORT", "5432"),
#         "HOST": os.environ.get("DB_TEST_HOST", "localhost"),
#         "ATOMIC_REQUESTS": True,
#     }
