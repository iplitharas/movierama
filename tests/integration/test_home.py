"""Integration test cases for the main homepage"""
import http

import pytest
from django.urls import reverse

from movies.models import Movie


@pytest.mark.django_db
def test_home_with_one_movie_no_user_logged_in(client, fake_user_with_one_movie):
    """
    Given a testing client, one user and one movie
    When I call the `home` page
    Then I'm expecting the `home page` with right content.
    """
    # Given 1 user with one movie review
    user, movie = fake_user_with_one_movie
    url = reverse("home")
    # When I access the homepage
    response = client.get(url)
    # Then
    assert response.status_code == http.HTTPStatus.OK
    response_content = str(response.content)
    # All the movie infos are rendered in the page
    assert movie.title in response_content
    assert movie.desc in response_content
    assert movie.genre not in response_content
    assert movie.year in response_content
    # User's name is listed as a url
    assert user.username.title() in response_content
    # But we aren't able to add any feedback
    assert "Like it" not in response_content
    assert "Dislike it" not in response_content
    # Or edit/delete the movie
    assert "Edit" not in response_content
    assert "Delete" not in response_content


@pytest.mark.django_db
def test_home_with_one_movie_user_logged_in(client, fake_user_with_one_movie):
    """
    Given a testing client one user and one movie
    When the user logs in
    Then I'm expecting the `home page` with right content
    """
    # Given 1 user with one movie review
    user, movie = fake_user_with_one_movie
    url_login = reverse("login")
    response = client.post(
        path=url_login, data={"username": user.username, "password": "password123"}
    )
    assert response.status_code == http.HTTPStatus.FOUND
    # When I access the homepage
    url = reverse("home")
    response = client.get(url)
    # Then
    assert response.status_code == http.HTTPStatus.OK
    response_content = str(response.content)
    # All the movie infos are rendered in the page
    assert movie.title in response_content
    assert movie.desc in response_content
    assert movie.genre not in response_content
    assert movie.year in response_content
    # We can only Logout
    assert "Hello " + user.username in response_content
    assert "Logout" in response_content
    # As the owner of the movie we can't add any feedback
    assert "Like it" not in response_content
    assert "Dislike it" not in response_content
    # But he can edit/delete it
    assert "Edit" in response_content
    assert "Delete" in response_content


@pytest.mark.django_db
def test_users_can_edit_their_movies(client, fake_user_with_one_movie):
    """
    Given a testing client, `one` user with movie
    When the sure `edits` the movie
    Then we're expecting the `home` page with right content
    """
    # Given 1 user with one movie review
    user, movie = fake_user_with_one_movie
    login_url = reverse("login")
    response = client.post(
        path=login_url, data={"username": user.username, "password": "password123"}
    )
    assert response.status_code == http.HTTPStatus.FOUND
    # When I access the homepage
    url = reverse("home")
    response = client.get(url)
    # Then
    assert response.status_code == http.HTTPStatus.OK
    response_content = str(response.content)
    # All the movie infos are rendered in the page
    assert movie.title in response_content
    assert movie.desc in response_content
    assert movie.genre not in response_content
    assert movie.year in response_content
    # Edit the movie
    edit_url = reverse("update-movie", args=[movie.id])
    response = client.post(
        edit_url, data={"title": "New title", "desc": "new", "year": "2023"}
    )
    assert response.status_code == http.HTTPStatus.FOUND
    response = client.get(url)
    response_content = str(response.content)
    assert movie.title not in response_content
    assert "New title" in response_content
    assert movie.desc not in response_content
    assert "new" in response_content
    assert movie.year not in response_content
    assert "2023" in response_content
    #
    movie.refresh_from_db()
    assert movie.title == "New title"
    assert movie.desc == "new"
    assert movie.year == "2023"


@pytest.mark.django_db
def test_users_can_delete_their_movies(client, fake_user_with_one_movie):
    """
    Given a testing client one user with one movie
    When the user selects one movie for deletion
    Then we expect the right content
    """
    # Given 1 user with one movie review
    user, movie = fake_user_with_one_movie
    login_url = reverse("login")
    response = client.post(
        path=login_url, data={"username": user.username, "password": "password123"}
    )
    assert response.status_code == http.HTTPStatus.FOUND
    # When I access the homepage
    url = reverse("home")
    response = client.get(url)
    # Then
    assert response.status_code == http.HTTPStatus.OK
    response_content = str(response.content)
    # All the movie infos are rendered in the page
    assert movie.title in response_content
    assert movie.desc in response_content
    assert movie.genre not in response_content
    assert movie.year in response_content
    assert Movie.objects.count() == 1
    # Edit the movie
    delete_url = reverse("delete-movie", args=[movie.id])
    response = client.post(delete_url)
    assert Movie.objects.count() == 0
    assert response.status_code == http.HTTPStatus.FOUND
    response = client.get(url)
    response_content = str(response.content)
    assert movie.title not in response_content
    assert "New title" not in response_content
    assert movie.desc not in response_content
    assert "new" not in response_content
    assert movie.year not in response_content
    assert "2023" not in response_content


@pytest.mark.django_db
def test_users_can_like_other_movies(client, fake_users_with_movies):
    """
    Given two users with one movie each
    When the first user likes the movie from the second user
    Then we expect the right content
    """
    # Given 2 user with one move each
    users, movies = fake_users_with_movies
    first_movie, second_movie = movies
    login_url = reverse("login")
    response = client.post(
        path=login_url, data={"username": users[0].username, "password": "password123"}
    )

    assert response.status_code == http.HTTPStatus.FOUND
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 0

    url = reverse("home")
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 0
    # When the first user likes the movie from the second user
    like_url = reverse("like-movie", args=[second_movie.id])
    client.post(like_url)
    url = reverse("home")
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 1</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_likes == 1
    assert second_movie.total_dislikes == 0


@pytest.mark.django_db
def test_users_can_dislike_other_movies(client, fake_users_with_movies):
    """
    Given two users with one movie each
    When the first user dislikes the movie from the second user
    Then we expect the right content
    """
    # Given 2 user with one move each
    users, movies = fake_users_with_movies
    first_movie, second_movie = movies
    login_url = reverse("login")
    response = client.post(
        path=login_url, data={"username": users[0].username, "password": "password123"}
    )

    assert response.status_code == http.HTTPStatus.FOUND
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 0
    url = reverse("home")
    response = client.get(url)
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 0
    # When the user dislikes the movie from the second user
    dislike_url = reverse("dislike-movie", args=[second_movie.id])
    # Then we expect the right content
    client.post(dislike_url)
    url = reverse("home")
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>1</p>" in response_content
    assert first_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 1


@pytest.mark.django_db
def test_users_can_revert_their_dislike_to_movie(client, fake_users_with_movies):
    """
    Given two users with one movie each
    When the first user has already disliked the movie from the second user
        and wants to revert it
    Then we expect the right content
    """
    #
    users, movies = fake_users_with_movies
    first_movie, second_movie = movies
    login_url = reverse("login")
    response = client.post(
        path=login_url, data={"username": users[0].username, "password": "password123"}
    )
    assert response.status_code == http.HTTPStatus.FOUND

    # When I access the homepage
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.OK
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 0

    # When the user dislikes the movie for the first time
    dislike_url = reverse("dislike-movie", args=[movies[1].id])
    client.post(dislike_url)
    url_home = reverse("home")
    response = client.get(url_home)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>1</p>" in response_content
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 1
    # Dislike for the second time
    client.post(dislike_url)
    url = reverse("home")
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 0


@pytest.mark.django_db
def test_users_can_revert_their_like(client, fake_users_with_movies):
    """
    Given two users with one movie each
    When the first user has already liked the movie from the second user
        and wants  to revert it
    Then we expect the right content
    """
    # Given 2 user with one move each
    users, movies = fake_users_with_movies
    first_movie, second_movie = movies
    login_url = reverse("login")
    response = client.post(
        path=login_url, data={"username": users[0].username, "password": "password123"}
    )
    assert response.status_code == http.HTTPStatus.FOUND

    # When I access the homepage
    url = reverse("home")
    response = client.get(url)
    # Then
    assert response.status_code == http.HTTPStatus.OK
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 0
    # First like
    like_url = reverse("like-movie", args=[movies[1].id])
    client.post(like_url)
    url = reverse("home")
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 1</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_likes == 1
    assert second_movie.total_dislikes == 0
    # Second like
    like_url = reverse("like-movie", args=[movies[1].id])
    client.post(like_url)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 0


@pytest.mark.django_db
def test_user_change_their_dislike_to_a_like(client, fake_users_with_movies):
    """
    Given two users with two movies
    When the fist user first dislike the movie (from the second user)
         and then change it to a like
    Then we expect the right content
    """
    # Given 2 user with one move each
    # where we have zero likes, dislikes on both of them
    users, movies = fake_users_with_movies
    first_movie, second_movie = movies
    login_url = reverse("login")
    response = client.post(
        path=login_url, data={"username": users[0].username, "password": "password123"}
    )
    assert response.status_code == http.HTTPStatus.FOUND
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 0
    url = reverse("home")
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    # When the first user dislikes the movie from the second user
    like_url = reverse("dislike-movie", args=[second_movie.id])
    client.post(like_url)
    url = reverse("home")
    response = client.get(url)
    response_content = str(response.content)
    # Then we have the right content
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>1</p>" in response_content
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 1
    # Also if they change the dislike to a like
    like_url = reverse("like-movie", args=[second_movie.id])
    client.post(like_url)
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 1
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 0
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 1</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content


@pytest.mark.django_db
def test_user_change_their_like_to_a_dislike(client, fake_users_with_movies):
    """
    Given two users with one movie each
    When the first user first like the movie (from the second user) and then dislikes it
    Then we expect the `home` page right content.
    """
    # Given 2 user with one move each
    # where we have zero likes, dislikes on both of them
    users, movies = fake_users_with_movies
    first_movie, second_movie = movies
    login_url = reverse("login")
    response = client.post(
        path=login_url, data={"username": users[0].username, "password": "password123"}
    )
    assert response.status_code == http.HTTPStatus.FOUND
    assert first_movie.total_likes == 0
    assert second_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_dislikes == 0
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.OK
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    # Once the second user likes the movie from the first user
    like_url = reverse("like-movie", args=[second_movie.id])
    client.post(like_url)
    url = reverse("home")
    response = client.get(url)
    response_content = str(response.content)
    # Then we have the right content
    assert "<strong>Likes:</strong> 1</p>" in response_content
    assert "<strong>Dislikes:</strong>0</p>" in response_content
    assert first_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_likes == 1
    assert second_movie.total_dislikes == 0
    # Also if the user change the like to a
    # dislike
    like_url = reverse("dislike-movie", args=[second_movie.id])
    client.post(like_url)
    # Then the number of likes decrease
    # and the number of dislikes increase
    response = client.get(url)
    response_content = str(response.content)
    assert "<strong>Likes:</strong> 0</p>" in response_content
    assert "<strong>Dislikes:</strong>1</p>" in response_content
    assert first_movie.total_likes == 0
    assert first_movie.total_dislikes == 0
    assert second_movie.total_likes == 0
    assert second_movie.total_dislikes == 1
