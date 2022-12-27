import os

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from movies.models import Movie

DEFAULT_ENGINE = "django.db.backends.sqlite3"

from typing import Any, List, Tuple


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


@pytest.fixture()
def fake_users_with_movies(fake_user_with_one_movie) -> Tuple[List[Any], List[Movie]]:
    first_user, first_movie = fake_user_with_one_movie

    # Create another user
    User = get_user_model()
    default_password = "password123"
    second_user = User(username="alice")
    second_user.save()

    second_movie = Movie.objects.create(
        author=second_user,
        title="Fight Club",
        desc="A depressed man (Edward Norton) suffering from insomnia meets a strange soap salesman named "
        "Tyler Durden (Brad Pitt) and soon finds himself living in his squalid "
        "house after his perfect apartment is destroyed. The two bored men form an "
        "underground club with strict rules and fight other men who are fed up with their"
        " mundane lives. Their perfect partnership frays when Marla (Helena Bonham Carter),"
        " a fellow support group crasher, attracts Tyler's attention.",
        genre="Thriller/Drama",
        year="1999",
    )

    return [first_user, second_user], [first_movie, second_movie]
