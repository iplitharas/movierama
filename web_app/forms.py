"""
Movie-model django form
"""
from django.forms import ModelForm
from movies.models import Movie


class MovieForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author", None)
        super(MovieForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Movie
        exclude = ["author", "likes", "dislikes"]
