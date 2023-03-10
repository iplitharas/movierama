# Generated by Django 4.1.4 on 2022-12-21 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the movie",
                        max_length=255,
                        verbose_name="Movie Title",
                    ),
                ),
                (
                    "desc",
                    models.TextField(
                        help_text="Description of the movie.",
                        verbose_name="Movie Description",
                    ),
                ),
                (
                    "genre",
                    models.CharField(
                        blank=True,
                        help_text="Optional genre of the movie ",
                        max_length=255,
                        verbose_name="Genre",
                    ),
                ),
                (
                    "year",
                    models.CharField(
                        help_text="Date of publication",
                        max_length=4,
                        verbose_name="Published Year",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("likes", models.IntegerField(help_text="Number of likes")),
                ("dislikes", models.IntegerField(help_text="Number of dislikes")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
