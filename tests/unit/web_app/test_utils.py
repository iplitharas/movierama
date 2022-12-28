"""Test cases for web/app utils helper functions"""
import pytest
from django.test.client import RequestFactory

from movies.models import Movie
from web_app.utils import apply_queryset_filtering


@pytest.mark.django_db
def test_apply_queryset_filtering_no_filtering(
    fake_user_with_one_movie, caplog
):  # pylint: disable=unused-argument)
    """
    Given a HTTP request and one movie
    When the user doesn't specify any filtering
    Then we're expecting the default query set
    """
    # Given
    caplog.clear()
    factory = RequestFactory()
    # When
    fake_request = factory.get("/")
    movie_qs = Movie.objects.get_queryset()
    movies = apply_queryset_filtering(request=fake_request, queryset=movie_qs)
    # Then
    assert movies.first() == movie_qs.first()


@pytest.mark.django_db
def test_apply_queryset_filtering_by_date(fake_users_with_movies, caplog):
    """
    Given a HTTP request and one movie
    When the user request the results filtered by `released_date`
    Then we're expecting a query set ordered by `year`
    """
    # Given
    caplog.clear()
    _, movies = fake_users_with_movies
    factory = RequestFactory()
    assert movies[0].year == "2011"
    assert movies[1].year == "1999"
    # When
    fake_request = factory.get("/?filter=released_date")
    movies_qs = apply_queryset_filtering(
        request=fake_request, queryset=Movie.objects.get_queryset()
    )
    # Then
    assert movies_qs[0].year == "1999"
    assert movies_qs[1].year == "2011"
    assert "released_date" in caplog.text


@pytest.mark.django_db
def test_apply_queryset_filtering_by_likes(fake_users_with_movies, caplog):
    """
    Given a HTTP request and one movie
    When the user request the results filtered by `likes`
    Then we're expecting a query set ordered by `total_likes`
    """
    # Given
    caplog.clear()
    users, movies = fake_users_with_movies
    factory = RequestFactory()
    movies[1].likes.add(users[0])
    movies[1].save()
    assert movies[0].total_likes == 0
    assert movies[1].total_likes == 1
    # When
    fake_request = factory.get("/?filter=likes")
    movie_qs = apply_queryset_filtering(
        request=fake_request, queryset=Movie.objects.get_queryset()
    )
    # Then
    assert movie_qs[0].total_likes == 1
    assert movie_qs[1].total_likes == 0
    assert "likes" in caplog.text


@pytest.mark.django_db
def test_apply_queryset_filtering_by_dislikes(fake_users_with_movies, caplog):
    """
    Given a HTTP request and one movie
    When the user request the results filtered by `dislikes`
    Then we're expecting a query set ordered by `total_dislikes`
    """
    # Given
    caplog.clear()
    users, movies = fake_users_with_movies
    factory = RequestFactory()
    movies[1].dislikes.add(users[0])
    movies[1].save()
    assert movies[0].total_dislikes == 0
    assert movies[1].total_dislikes == 1
    # When
    fake_request = factory.get("/?filter=dislikes")
    movie_qs = apply_queryset_filtering(
        request=fake_request, queryset=Movie.objects.get_queryset()
    )
    # Then
    assert movie_qs[0].total_dislikes == 1
    assert movie_qs[1].total_dislikes == 0
    assert "dislikes" in caplog.text


@pytest.mark.django_db
def test_apply_queryset_filtering_by_current_user(fake_users_with_movies, caplog):
    """
    Given a `HTTP request` two users with one movie each
    When the user request the results filtered by `by_current_user`
    Then we're expecting a query set ordered by the right user
    """
    # Given
    caplog.clear()
    users, _ = fake_users_with_movies
    factory = RequestFactory()
    # When
    fake_request = factory.get("/?filter=by_current_user")
    fake_request.user = users[0]
    # Then
    movie_qs = apply_queryset_filtering(
        request=fake_request, queryset=Movie.objects.get_queryset()
    )
    assert movie_qs.count() == 1
    assert "by_current_user" in caplog.text


@pytest.mark.django_db
def test_apply_queryset_filtering_by_author(fake_users_with_movies, caplog):
    """
    Given a `HTTP request` two users with one movie each
    When the user request the results filtered by `author`
    Then we're expecting a query set ordered by the right user
    """
    # Given
    caplog.clear()
    users, _ = fake_users_with_movies
    factory = RequestFactory()
    # When
    fake_request = factory.get(f"/?author={users[0].id}")
    fake_request.user = users[0]
    # Then
    movie_qs = apply_queryset_filtering(
        request=fake_request, queryset=Movie.objects.get_queryset()
    )
    assert movie_qs.count() == 1
    assert "author" in caplog.text
