"""Helper function for the test cases"""
import http

from django.urls import reverse


def login_user(client, user) -> None:
    """
    helper function to perform a login for the  `user`
    """
    url_login = reverse("login")
    response = client.post(
        path=url_login,
        data={"username": user.username, "password": "password123"},
    )
    assert response.status_code == http.HTTPStatus.FOUND
