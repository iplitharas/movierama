import http

import pytest
from django.contrib.auth import get_user_model
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
def test_home_with_one_movie(client, fake_user_with_one_movie):
    """
    Given a testing client
    When I call the home page with one user
    Then I'm expecting the home page with the right title
    """
    user, movie = fake_user_with_one_movie
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.OK
    response_content = str(response.content)
    assert movie.title in response_content
    assert movie.desc in response_content
    assert movie.genre not in response_content
    assert movie.year in response_content
    assert user.username.title() in response_content


@pytest.mark.django_db
def test_home_without_a_user_logged(client):
    """
    Given a testing client
    When I call the `home` page without any user logged in
    Then I'm expecting the `Login` `Signup` in the content of
    the home page
    """
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.OK
    assert "Login" in str(response.content)
    assert "Signup" in str(response.content)
    assert "hi" not in str(response.content)
