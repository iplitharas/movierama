# Generated by Django 4.1.4 on 2022-12-21 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="movie",
            name="dislikes",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="likes",
        ),
    ]
