import http

import pytest
from django.urls import reverse

from movies.models import Movie


@pytest.mark.django_db
def test_list_movie(client, fake_user_with_one_movie):
    """
    Given  one movie
    When we call the `api/movies/v1/` endpoint
        from any user(authenticated/non-authenticated)
    Then we expect the right response content
    """
    # Given
    user, movie = fake_user_with_one_movie
    movies = Movie.objects.all()
    assert len(movies) == 1
    # When
    response = client.get(reverse("movies"))
    # Then
    assert response.status_code == http.HTTPStatus.OK
    assert response.data[0]["title"] == movie.title
    assert response.data[0]["desc"] == movie.desc
    assert response.data[0]["genre"] == movie.genre
    assert response.data[0]["genre"] == movie.genre
    assert response.data[0]["year"] == movie.year
    assert response.data[0]["likes"] == []
    assert response.data[0]["dislikes"] == []
