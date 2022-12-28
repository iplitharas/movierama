import http

import pytest
from django.urls import reverse

from movies.models import Movie
from tests.utils import login_user


@pytest.mark.django_db
def test_edit_movie_user_authenticated(client, fake_user_with_one_movie):
    """
    Given one movie
    When we call the `api/movies/v1/new` endpoint
        from an authenticated user with a PATCH request
    Then we expect a `http.HTTPStatus.OK=200`
    """
    # Given
    faker_user, movie = fake_user_with_one_movie
    assert Movie.objects.count() == 1
    # When
    login_user(client=client, user=faker_user)
    api_movies_detail_url = reverse("movies-detail", args=[movie.id])
    response = client.patch(
        path=api_movies_detail_url,
        data={
            "title": "New movie title",
        },
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.OK
    assert response.data == {
        "title": "New movie title",
        "desc": movie.desc,
        "genre": movie.genre,
        "year": movie.year,
        "author": movie.author.id,
        "likes": [],
        "dislikes": [],
        "id": movie.id,
    }
    assert Movie.objects.count() == 1


@pytest.mark.django_db
def test_delete_movie_user_authenticated(client, fake_user_with_one_movie):
    """
    Given one movie
    When we call the `api/movies/v1/new` endpoint
        from an authenticated user with a delete request
    Then we expect a `http.HTTPStatus.NO_CONTENT=204`
    """
    # Given
    faker_user, movie = fake_user_with_one_movie
    assert Movie.objects.count() == 1
    # When
    login_user(client=client, user=faker_user)
    api_movies_detail_url = reverse("movies-detail", args=[movie.id])
    response = client.delete(
        path=api_movies_detail_url,
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.NO_CONTENT
    assert Movie.objects.count() == 0


@pytest.mark.django_db
def test_get_movie_user_authenticated(client, fake_user_with_one_movie):
    """
    Given one movie
    When we call the `api/movies/v1/new` endpoint
        from an authenticated user with a GET request
    Then we expect a `http.HTTPStatus.OK=200`
    """
    # Given
    faker_user, movie = fake_user_with_one_movie
    assert Movie.objects.count() == 1
    # When
    login_user(client=client, user=faker_user)
    api_movies_detail_url = reverse("movies-detail", args=[movie.id])
    response = client.get(
        path=api_movies_detail_url,
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.OK
    assert response.data == {
        "title": movie.title,
        "desc": movie.desc,
        "genre": movie.genre,
        "year": movie.year,
        "author": movie.author.id,
        "likes": [],
        "dislikes": [],
        "id": movie.id,
    }
    assert Movie.objects.count() == 1


@pytest.mark.django_db
def test_get_detail_user_non_authenticated_user(client, fake_user_with_one_movie):
    """
    Given an non-authenticated user
    When we try to access the `api/movies/v1/{id}
    THEN we expect an `http.HTTPStatus.OK`
    """
    # Given
    _, movie = fake_user_with_one_movie
    api_movies_detail_url = reverse("movies-detail", args=[movie.id])
    # When
    response = client.get(
        path=api_movies_detail_url,
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.OK
    assert response.data == {
        "title": movie.title,
        "desc": movie.desc,
        "genre": movie.genre,
        "year": movie.year,
        "author": movie.author.id,
        "likes": [],
        "dislikes": [],
        "id": movie.id,
    }
    assert Movie.objects.count() == 1


@pytest.mark.django_db
def test_edit_detail_user_non_authenticated_user(client, fake_user_with_one_movie):
    """
    Given an non-authenticated user
    When we try to access the `api/movies/v1/{id}
        with a `PATCH` request
    THEN we expect an `HTTPStatus.FORBIDDEN`
    """
    # Given
    _, movie = fake_user_with_one_movie
    api_movies_detail_url = reverse("movies-detail", args=[movie.id])
    # When
    response = client.patch(
        path=api_movies_detail_url,
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.FORBIDDEN
    assert Movie.objects.count() == 1


@pytest.mark.django_db
def test_delete_detail_user_non_authenticated_user(client, fake_user_with_one_movie):
    """
    Given an non-authenticated user
    When we try to access the `api/movies/v1/{id} with
        a DELETE request
    THEN we expect a `.HTTPStatus.FORBIDDEN`
    """
    # Given
    _, movie = fake_user_with_one_movie
    api_movies_detail_url = reverse("movies-detail", args=[movie.id])
    # When
    response = client.patch(
        path=api_movies_detail_url,
        content_type="application/json",
    )
    # Then
    assert response.status_code == http.HTTPStatus.FORBIDDEN
    assert Movie.objects.count() == 1
