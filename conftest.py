"""Common pytest fixtures"""
from typing import Any, List, Tuple

import pytest
from django.contrib.auth import get_user_model

from movies.models import Movie

DEFAULT_ENGINE = "django.db.backends.sqlite3"


@pytest.fixture(name="fake_user_with_one_movie")
def fake_user_with_one_movie_fixture() -> Tuple[Movie, Any]:
    """pytest fixture for creating one user with one movie"""
    User = get_user_model()  # pylint: disable=invalid-name
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


@pytest.fixture(name="fake_user")
def fake_user_fixture():
    """pytest fixture for creating a fake user"""
    User = get_user_model()  # pylint: disable=invalid-name
    default_password = "password123"
    user = User(username="bob")
    user.set_password(default_password)
    user.save()
    return user


@pytest.fixture(name="fake_users_with_movies")
def fake_users_with_movies_fixture(
    fake_user_with_one_movie,
) -> Tuple[List[Any], List[Movie]]:
    """pytest fixture for creating two users with one movie each"""
    first_user, first_movie = fake_user_with_one_movie
    # Create another user
    User = get_user_model()  # pylint: disable=invalid-name
    default_password = "password123"
    second_user = User(username="alice")
    second_user.set_password(default_password)
    second_user.save()
    second_movie = Movie.objects.create(
        author=second_user,
        title="Fight Club",
        desc="A depressed man (Edward Norton) suffering from insomnia "
        "meets a strange soap salesman named "
        "Tyler Durden (Brad Pitt) and soon finds himself living in his squalid "
        "house after his perfect apartment is destroyed. The two bored men form an "
        "underground club with strict rules and fight other men who are fed up with their"
        " mundane lives. Their perfect partnership frays when Marla (Helena Bonham Carter),"
        " a fellow support group crasher, attracts Tyler's attention.",
        genre="Thriller/Drama",
        year="1999",
    )

    return [first_user, second_user], [first_movie, second_movie]
