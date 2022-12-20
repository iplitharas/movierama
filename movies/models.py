from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the movie")
    desc = models.CharField(max_length=2024, help_text="Description of the movie.")
    genre = models.CharField(
        max_length=255, blank=True, help_text="Optional genre of the movie "
    )
    year = models.CharField(max_length=4, help_text="Date of publication")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(help_text="Number of likes")
    dislikes = models.IntegerField(help_text="Number of dislikes")

    def __str__(self) -> str:
        return f"{self.title}"
