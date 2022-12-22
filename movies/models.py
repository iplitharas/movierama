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
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="movie_likes",
        verbose_name="Users who liked this a movie",
        help_text="Many user can like this movie and this movie can be liked from different users",
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="movie_dislikes",
        verbose_name="Users who don't this a movie",
        help_text="Many user can dislike this movie and this movie can be disliked from different users",
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    cover = models.ImageField(
        upload_to="covers/",
        verbose_name="Movie cover image",
        blank=True,
        help_text="Optional cover image",
    )
    objects = MovieManager()

    def __str__(self) -> str:
        return f"{self.title} by {self.author.username}"

    @property
    def total_likes(self) -> int:
        return self.likes.count()

    @property
    def total_dislikes(self) -> int:
        return self.dislikes.count()



