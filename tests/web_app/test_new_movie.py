"""
Test cases for the `new-movie` endpoint.
"""
import http

import pytest
from django.urls import reverse

from movies.models import Movie
from tests.utils import login_user


@pytest.mark.django_db
def test_new_movie_success(client, fake_user, caplog):
    """
    Given one authenticated user without any movie
    When the user POSTS at the `new-movie` endpoint
    Then we expect the movie in the db
    """
    caplog.clear()
    # Given
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 0
    # When
    new_movie_url = reverse("new-movie")
    response = client.post(
        new_movie_url,
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
    assert "Successfully" in caplog.text


@pytest.mark.django_db
def test_new_movie_with_invalid_form_data(client, fake_user, caplog):
    """
    Given one authenticated user without any movie
    When the user makes a POST request at the  `new-movie`
    endpoint with some missing mandatory fields
    Then we expect an empty new form
    """
    caplog.clear()
    # Given
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 0
    # When
    new_movie_url = reverse("new-movie")

    response = client.post(
        new_movie_url,
        data={"desc": "some description", "genre": "some genre", "year": "2023"},
    )
    # Then
    assert response.status_code == http.HTTPStatus.OK
    assert Movie.objects.count() == 0
    assert "Cannot create a new movie" in caplog.text
    assert "New Movie" in str(response.content)


@pytest.mark.django_db
def test_new_movie_get_request(client, fake_user, caplog):
    """
    Given one authenticated user without any movie
    When the user calls the `new-movie` endpoint with a `GET`
    Then we expect an empty new form.
    """
    caplog.clear()
    # Given
    login_user(client=client, user=fake_user)
    assert Movie.objects.count() == 0
    # When
    new_movie_url = reverse("new-movie")

    response = client.get(
        new_movie_url,
    )
    # Then
    assert response.status_code == http.HTTPStatus.OK
    assert Movie.objects.count() == 0
    assert "New Movie" in str(response.content)


@pytest.mark.django_db
def test_new_movie_get_non_authenticated_users(client):
    """
    Given a testing client
    When the user is non-authenticated
    Then we expect a redirect to the `home` page
    """
    # Given when
    new_movie_url = reverse("new-movie")
    response = client.get(
        new_movie_url,
    )
    # Then
    assert response.status_code == http.HTTPStatus.FOUND
    assert Movie.objects.count() == 0
