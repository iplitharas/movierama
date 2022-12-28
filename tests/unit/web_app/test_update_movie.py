"""
Test cases for the `new-movie` endpoint.
"""
import http

import pytest
from django.urls import reverse

from movies.models import Movie
from tests.utils import login_user


@pytest.mark.django_db
def test_update_movie_success(client, fake_user_with_one_movie, caplog):
    """
    Given one authenticated user with a movie
    When the user POSTS at the `update-movie` endpoint
    Then we expect the movie to be updated
    """
    caplog.clear()
    fake_user, movie = fake_user_with_one_movie
    # Given
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 1
    assert movie.title == "Harry Potter and the Deathly Hallows: Part 2"
    # When
    update__movie_url = reverse("update-movie", args=[movie.id])

    response = client.post(
        update__movie_url,
        data={
            "title": "New movie title",
            "desc": "some description",
            "genre": "some genre",
            "year": "2023",
        },
    )
    # Then
    assert response.status_code == http.HTTPStatus.FOUND
    assert Movie.objects.count() == 1
    movie.refresh_from_db()
    assert movie.title == "New movie title"
    assert "Successfully" in caplog.text


@pytest.mark.django_db
def test_update_movie_with_invalid_form(client, fake_user_with_one_movie, caplog):
    """
    Given one authenticated user with a movie
    When the user makes a POST request at the `update-movie` endpoint
        with an invalid form
    Then we expect a redirect to the `home-page`
    """
    caplog.clear()
    fake_user, movie = fake_user_with_one_movie
    # Given
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 1
    assert movie.title == "Harry Potter and the Deathly Hallows: Part 2"
    # When
    update__movie_url = reverse("update-movie", args=[movie.id])

    response = client.post(
        update__movie_url,
        data={
            "title": "",
            "desc": "",
            "genre": "",
            "year": "",
        },
    )
    # Then
    assert response.status_code == http.HTTPStatus.FOUND
    assert Movie.objects.count() == 1
    movie.refresh_from_db()
    assert movie.title == "Harry Potter and the Deathly Hallows: Part 2"
    assert "Cannot update a new movie" in caplog.text


@pytest.mark.django_db
def test_update_movie_with_wrong_movie_id(client, fake_user_with_one_movie):
    """
    Given one authenticated user with a movie
    When the user POSTS at the `update-movie` endpoint with a
        invalid movie_id
    Then we expect a `HTTP_NOT_FOUND` response
    """
    fake_user, _ = fake_user_with_one_movie
    # Given
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 1
    # When
    update__movie_url = reverse("update-movie", args=[99999])

    response = client.post(
        update__movie_url,
        data={
            "title": "New movie title",
            "desc": "some description",
            "genre": "some genre",
            "year": "2023",
        },
    )
    # Then
    assert response.status_code == http.HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_movie_without_permissions(client, fake_users_with_movies):
    """
    Given one authenticated user with a movie
    When the user POSTS at the `update-movie` endpoint with a
        valid movie_id but without permissions
        needs to be the author
    Then we expect a `HTTP_NOT_FOUND` response
    """
    users, movies = fake_users_with_movies
    first_user, _ = users
    _, second_movie = movies
    # Given
    login_user(client=client, user=first_user)
    assert Movie.objects.count() == 2
    # When
    update_movie_url = reverse("update-movie", args=[second_movie.id])

    response = client.post(
        update_movie_url,
        data={
            "title": "New movie title",
            "desc": "some description",
            "genre": "some genre",
            "year": "2023",
        },
    )
    # Then
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_update_movie_non_authenticated_user(client, fake_user_with_one_movie):
    """
    Given a non-authenticated user
    When we try a POST request at the `update-movie` endpoint
    Then we expect a redirection to the `login` home page.
    """
    _, movie = fake_user_with_one_movie
    assert Movie.objects.count() == 1
    # When
    update_movie_url = reverse("update-movie", args=[movie.id])
    response = client.post(
        update_movie_url,
        data={
            "title": "New movie title",
            "desc": "some description",
            "genre": "some genre",
            "year": "2023",
        },
    )
    # Then
    assert response.status_code == http.HTTPStatus.FOUND
