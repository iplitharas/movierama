"""Test cases for Movie Manager"""
import pytest
from django.contrib.auth import get_user_model

from movies.models import Movie


@pytest.mark.django_db
def test_get_movies_by_author(fake_user):
    """
    Given two users with one movie each
    When I filter the movies `by_author`
    Then I'm expecting only one
    """
    # Given
    User = get_user_model()  # pylint: disable=invalid-name
    default_password = "password123"
    user = User(username="test-user")
    user.set_password(default_password)
    user.save()
    Movie.objects.create(author=fake_user, title="some movie", year="2022")
    Movie.objects.create(author=user, title="some other movie", year="2023")
    # When/Then
    assert Movie.objects.by_author(author=user).count() == 1


@pytest.mark.django_db
def test_get_movies_by_published_date(fake_user):
    """
    Given two users with one movie each
    When I filter the movies `by_published_date`
    Then I'm expecting two movies year by date (descending ordering)
    """
    # Given
    User = get_user_model()  # pylint: disable=invalid-name
    default_password = "password123"
    user = User(username="test-user")
    user.set_password(default_password)
    user.save()
    first_movie = Movie.objects.create(
        author=fake_user, title="some movie", year="1000"
    )
    second_movie = Movie.objects.create(
        author=user, title="some other movie", year="2023"
    )
    # When/Then
    assert first_movie.year < second_movie.year
    assert Movie.objects.by_published_date().count() == 2
    assert Movie.objects.by_published_date().first() == first_movie
    assert Movie.objects.by_published_date().last() == second_movie


@pytest.mark.django_db
def test_get_movies_by_total_likes(fake_user):
    """
    Given two users with one movie each
    When I filter the movies `by_likes`
    Then I'm expecting a queryset ordered by number of likes
        in ascending order
    """
    # Given
    User = get_user_model()  # pylint: disable=invalid-name
    default_password = "password123"
    user = User(username="test-user")
    user.set_password(default_password)
    user.save()
    first_movie = Movie.objects.create(
        author=fake_user, title="some movie", year="2023"
    )
    assert first_movie.total_likes == 0
    second_movie = Movie.objects.create(
        author=user, title="some other movie", year="2023"
    )
    second_movie.likes.add(fake_user)
    second_movie.save()
    # When/Then
    assert second_movie.total_likes == 1
    assert second_movie.total_likes == 1
    assert Movie.objects.by_likes().count() == 2
    assert Movie.objects.by_likes().first() == second_movie
    assert Movie.objects.by_likes().last() == first_movie


@pytest.mark.django_db
def test_get_movies_by_total_dislikes(fake_user):
    """
    Given two users with one movie each
    When I filter the movies `by_dislikes`
    Then I'm expecting a `queryset` ordered by number of dislikes
         in ascending order
    """
    # Given
    User = get_user_model()  # pylint: disable=invalid-name
    default_password = "password123"
    user = User(username="test-user")
    user.set_password(default_password)
    user.save()
    first_movie = Movie.objects.create(
        author=fake_user, title="some movie", year="2023"
    )
    assert first_movie.total_dislikes == 0
    second_movie = Movie.objects.create(
        author=user, title="some other movie", year="2023"
    )
    second_movie.dislikes.add(fake_user)
    second_movie.save()
    # When/Then
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 1
    assert Movie.objects.by_dislikes().count() == 2
    assert Movie.objects.by_dislikes().first() == second_movie
    assert Movie.objects.by_dislikes().last() == first_movie
