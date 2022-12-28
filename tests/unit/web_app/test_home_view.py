"""Test cases for the web-app home endpoint"""
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
