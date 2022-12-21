from django.db import models

from config import settings
from movies.movie_manager import MovieManager


class Movie(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name="Movie Title", max_length=255, help_text="Title of the movie"
    )
    desc = models.TextField(
        verbose_name="Movie Description", help_text="Description of the movie."
    )
    genre = models.CharField(
        verbose_name="Genre",
        max_length=255,
        blank=True,
        help_text="Optional genre of the movie ",
    )
    year = models.CharField(
        verbose_name="Published Year", max_length=4, help_text="Date of publication"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = MovieManager()

    def __str__(self) -> str:
        return f"{self.title}"
