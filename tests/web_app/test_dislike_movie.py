import http

import pytest
from django.urls import reverse

from movies.models import Movie
from tests.utils import login_user


@pytest.mark.django_db
def test_dislike_movie_endpoint_first_time(client, fake_users_with_movies, caplog):
    """
    Given two users with one movie each
    When the first user 'likes' the movie from the second user
    Then we expect a redirection to the `homepage` and the
        right count of total dislikes and the right log message
    """
    caplog.clear()
    users, movies = fake_users_with_movies
    first_user, _ = users
    first_movie, second_movie = movies
    # Given
    login_user(client=client, user=first_user)
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 0
    # When
    dislike_movie_url = reverse("dislike-movie", args=[second_movie.id])
    response = client.post(dislike_movie_url)
    # Then
    assert response.status_code == http.HTTPStatus.FOUND
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 1
    assert "Added a dislike from user" in caplog.text


@pytest.mark.django_db
def test_dislike_movie_endpoint_second_time(client, fake_users_with_movies, caplog):
    """
    Given two users with one movie each
    When the first user 'dislikes' the movie for the second time
        from the second user
    Then we expect a redirection to the `homepage`, the
        right count of total dislikes=0, and the right log message
    """

    # Given
    caplog.clear()
    users, movies = fake_users_with_movies
    first_user, _ = users
    first_movie, second_movie = movies
    # User has already liked the movie
    second_movie.dislikes.add(first_user)
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 1
    login_user(client=client, user=first_user)
    # When
    dislike_movie_url = reverse("dislike-movie", args=[second_movie.id])
    response = client.post(dislike_movie_url)
    assert response.status_code == http.HTTPStatus.FOUND
    # Then
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 0
    assert "Reverted dislike from use" in caplog.text


@pytest.mark.django_db
def test_dislike_movie_endpoint_with_a_like(client, fake_users_with_movies, caplog):
    """
    Given two users with one movie each
    When the first user 'dislikes' the movie with a previous
    `like`
    Then we expect a redirection to the `homepage`, the
        right count of total dislikes=1, and the right log message
    """

    # Given
    caplog.clear()
    users, movies = fake_users_with_movies
    first_user, _ = users
    first_movie, second_movie = movies
    login_user(client=client, user=first_user)
    # User has already liked the movie
    second_movie.likes.add(first_user)
    assert second_movie.total_likes == 1
    assert second_movie.total_dislikes == 0
    # When
    dislike_movie_url = reverse("dislike-movie", args=[second_movie.id])
    response = client.post(dislike_movie_url)
    assert response.status_code == http.HTTPStatus.FOUND
    # Then
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 1
    assert "deleted the like" in caplog.text


@pytest.mark.django_db
def test_dislike_movie_non_authenticated_user(client, fake_user_with_one_movie):
    """
    Given a non-authenticated user
    When we try a POST request at the `dislike-movie` endpoint
    Then we expect a redirection to the `login` home page.
    """
    _, movie = fake_user_with_one_movie
    assert Movie.objects.count() == 1
    # When
    dislike_movie_url = reverse("dislike-movie", args=[movie.id])
    response = client.post(dislike_movie_url)
    # Then
    assert response.status_code == http.HTTPStatus.FOUND


@pytest.mark.django_db
def test_dislike_movie_users_cannot_dislike_their_own_movies(
    client, fake_user_with_one_movie
):
    """
    Given an authenticated user
    When we make a POST request to the `dislike-movie` endpoint
        with the `movie-id` which belongs to the same user
        who makes the request
    Then we expect an `http.Unauthorized` response
    """
    fake_user, movie = fake_user_with_one_movie
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 1
    # When
    dislike_movie_url = reverse("dislike-movie", args=[movie.id])
    response = client.post(dislike_movie_url)
    # Then
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_dislike_movie_with_wrong_movie_id(client, fake_user_with_one_movie):
    """
    Given one authenticated user with a movie
    When the user POSTS at the `dislike-movie` endpoint with a
        invalid movie_id
    Then we expect a `HTTP_NOT_FOUND` response
    """
    # Given
    fake_user, movie = fake_user_with_one_movie
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 1
    # When
    dislike_movie_url = reverse("dislike-movie", args=[99999])
    response = client.post(dislike_movie_url)
    # Then
    assert response.status_code == http.HTTPStatus.NOT_FOUND
