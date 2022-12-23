import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_login_with_valid_credentials(client):
    """
    Given a testing client
    When I log in with the right credentials
    Then I'm expecting `True` from client.login
    """
    # Given a user
    User = get_user_model()
    default_password = "pytest-s3cr3T"
    user = User(username="pytest_user")
    user.set_password(default_password)
    user.save()
    # When we try to login with the right password
    logged_in = client.login(username=user.username, password=default_password)
    # Then we are in!
    assert logged_in


@pytest.mark.django_db
def test_login_with_invalid_credentials(client):
    """
    Given a testing client
    When I log in with the wrong credentials
    Then I'm expecting `False` from client.login
    """
    # Given a user
    User = get_user_model()
    default_password = "pytest-s3cr3T"
    user = User(username="pytest_user")
    user.set_password(default_password)
    user.save()
    # When we try to login with the wrong password
    logged_in = client.login(username=user.username, password="password")
    # Then we aren't able.
    assert not logged_in
