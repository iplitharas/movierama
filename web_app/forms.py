"""
Movie-model django form
"""
from django.forms import ModelForm

from movies.models import Movie


class MovieForm(ModelForm):  # pylint: disable=missing-class-docstring
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Movie
        exclude = [  # pylint: disable=modelform-uses-exclude
            "author",
            "likes",
            "dislikes",
        ]
