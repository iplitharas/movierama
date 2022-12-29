"""
Test cases for the `delete-movie` web-app endpoint.
"""
import http

import pytest
from django.urls import reverse

from movies.models import Movie
from tests.utils import login_user


@pytest.mark.django_db
def test_delete_movie_success(client, fake_user_with_one_movie, caplog):
    """
    Given one authenticated user with a movie
    When the user make a POST request at
        the `delete-movie` endpoint
    Then we expect the movie to be deleted
    """
    caplog.clear()
    # Given
    faker_user, movie = fake_user_with_one_movie
    login_user(client=client, user=faker_user)
    assert Movie.objects.count() == 1
    # When
    update__movie_url = reverse("delete-movie", args=[movie.id])
    response = client.post(
        update__movie_url,
    )
    # Then
    assert response.status_code == http.HTTPStatus.FOUND
    assert Movie.objects.count() == 0
    assert "Successfully deleted the movie" in caplog.text


@pytest.mark.django_db
def test_delete_movie_with_wrong_movie_id(client, fake_user_with_one_movie):
    """
    Given one authenticated user with one movie
    When the user makes a `POST` request at the `delete-movie` endpoint with a
            invalid `movie_id`
    Then we expect a `HTTP_NOT_FOUND` response
    """
    # Given
    faker_user, _ = fake_user_with_one_movie
    login_user(client=client, user=faker_user)
    assert Movie.objects.count() == 1
    # When
    delete_movie_url = reverse("delete-movie", args=[99999])
    response = client.post(
        delete_movie_url,
    )
    # Then
    assert response.status_code == http.HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_movie_without_permissions(client, fake_users_with_movies):
    """
    Given one authenticated user with one movie
    When the user makes a `POST` request at the `delete-movie` endpoint
         with a valid movie_id but without permissions
        (needs to be the author)
    Then we expect a `UNAUTHORIZED` response
    """
    # Given
    users, movies = fake_users_with_movies
    first_user, _ = users
    _, second_movie = movies
    login_user(client=client, user=first_user)
    assert Movie.objects.count() == 2
    # When
    # `first_user` has permission for deletion only on the
    # `first_movie`
    delete_movie_url = reverse("delete-movie", args=[second_movie.id])
    response = client.post(
        delete_movie_url,
    )
    # Then
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert Movie.objects.count() == 2


@pytest.mark.django_db
def test_delete_movie_non_authenticated_user(client, fake_user_with_one_movie):
    """
    Given a non-authenticated user
    When we try a `POST` request at the `delete-movie` endpoint
    Then we expect a redirection to the `login` home page without
    a successful deletion.
    """
    _, movie = fake_user_with_one_movie
    assert Movie.objects.count() == 1
    # When
    update_movie_url = reverse("delete-movie", args=[movie.id])
    response = client.post(update_movie_url)
    # Then
    assert response.status_code == http.HTTPStatus.FOUND
    assert Movie.objects.count() == 1


@pytest.mark.django_db
def test_delete_movie_get_request(client, fake_user_with_one_movie, caplog):
    """
    Given one authenticated user with one movie
    When the user calls the `delete-movie` endpoint with a `GET`
    Then we expect an empty new form.
    """
    # Given
    fake_user, movie = fake_user_with_one_movie
    caplog.clear()
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 1
    # When
    delete_movie_url = reverse("delete-movie", args=[movie.id])
    response = client.get(delete_movie_url)
    # Then
    assert response.status_code == http.HTTPStatus.OK
    assert Movie.objects.count() == 1
    assert "Delete Movie" in str(response.content)
