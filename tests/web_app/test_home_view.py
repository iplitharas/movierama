import http

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_title(client):
    """
    Given a testing client
    When I call the home page
    Then I'm expecting the home page with the right title
    """
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.OK
    # verify the right templates are rendered
    assert response.template_name == ["movies/home.html", "movies/movie_list.html"]
    assert "movierama" in str(response.content)


@pytest.mark.django_db
def test_home_without_a_user_logged(client):
    """
    Given a testing client
    When I call the `home` page without any user logged in
    Then I'm expecting the `Login` && `Signup` in the content of
    the `home` page
    """
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.OK
    assert "Login" in str(response.content)
    assert "Signup" in str(response.content)
    assert "hi" not in str(response.content)


@pytest.mark.django_db
def test_home_with_one_movie(client, fake_user_with_one_movie):
    """
    Given a testing client one user and one movie
    When I call the `home` page
    Then I'm expecting the home page with right content
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
    Given a testing client one user with movie
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
