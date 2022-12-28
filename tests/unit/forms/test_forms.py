"""Test cases for `MovieForm`"""
import pytest

from web_app.forms import MovieForm


@pytest.mark.parametrize(
    "form_input,expected",
    [
        ({}, False),
        ({"title": "Only title"}, False),
        ({"title": "Only title", "desc": "some description"}, False),
        ({"title": "Only title", "desc": "some description", "year": "123"}, True),
        (
            {
                "title": "Only title",
                "desc": "some description",
                "year": "123",
                "genre": "Comedy",
            },
            True,
        ),
    ],
)
def test_movie_form(form_input, expected):
    """
    Make sure the `MovieForm` check the right model fields
    """
    movie_form = MovieForm(data=form_input)
    assert movie_form.is_valid() == expected
