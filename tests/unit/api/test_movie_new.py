"""Test cases for the `api/v1/movies/new"""

import http

import pytest
from django.urls import reverse

from movies.models import Movie
from tests.utils import login_user


@pytest.mark.django_db
def test_add_new_movie_user_authenticated(client, fake_user_with_one_movie):
    """
    Given one movie
    When we call the `api/movies/v1/new` endpoint
        from an authenticated user
    Then we expect the right response and a new movie created
    """
    # Given
    faker_user, movie = fake_user_with_one_movie
    assert Movie.objects.count() == 1
    # When
    login_user(client=client, user=faker_user)
    api_movies_add_url = reverse("movies-new")
    response = client.post(
        path=api_movies_add_url,
        data={
            "title": "New movie title",
            "desc": "New movie description",
            "genre": "New genre",
            "year": "1999",
        },
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.data == {
        "title": "New movie title",
        "desc": "New movie description",
        "genre": "New genre",
        "year": "1999",
        "likes": [],
        "dislikes": [],
        "id": movie.id + 1,
    }
    assert Movie.objects.count() == 2


@pytest.mark.django_db
def test_add_new_movie_user_authenticated_update_likes(
    client, fake_user_with_one_movie
):
    """
    Given one movie
    When we call the `api/movies/v1/new` endpoint
        from an authenticated user with some number of likes
    Then we expect the right response (ignoring any number of likes)
     and a new movie created
    """
    # Given
    faker_user, movie = fake_user_with_one_movie
    assert Movie.objects.count() == 1
    # When
    login_user(client=client, user=faker_user)
    api_movies_add_url = reverse("movies-new")
    response = client.post(
        path=api_movies_add_url,
        data={
            "title": "New movie title",
            "desc": "New movie description",
            "genre": "New genre",
            "year": "1999",
            "likes": [100],
        },
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.data == {
        "title": "New movie title",
        "desc": "New movie description",
        "genre": "New genre",
        "year": "1999",
        "likes": [],
        "dislikes": [],
        "id": movie.id + 1,
    }
    assert Movie.objects.count() == 2


@pytest.mark.django_db
def test_add_new_movie_user_non_authenticated(client):
    """
    Given one movie
    When we call the `api/movies/v1/new` endpoint
        from an non-authenticated user
    Then we expect a `http.HTTPStatus.FORBIDDEN`
    """
    # Given
    assert Movie.objects.count() == 0
    # When
    api_movies_add_url = reverse("movies-new")
    response = client.post(
        path=api_movies_add_url,
        data={
            "title": "New movie title",
            "desc": "New movie description",
            "genre": "New genre",
            "author": -1,
            "year": "1999",
            "likes": [],
            "dislikes": [],
        },
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.FORBIDDEN
    assert Movie.objects.count() == 0
