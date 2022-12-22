from django.db import models
from django.db.models import F, Count

from accounts.models import CustomUser


class MovieQuerySet(models.QuerySet):
    def by_author(self, author: CustomUser):
        return self.filter(author=author)

    def by_published_date(self):
        return self.order_by("year")

    def by_likes(self):
        return self.annotate(tmp=Count("likes")).order_by("-tmp")

    def by_dislikes(self):
        # by default the order is ascending
        # `-` reverse that
        return self.annotate(tmp=Count("dislikes")).order_by("-tmp")


class MovieManager(models.Manager):
    def get_queryset(self):
        return MovieQuerySet(self.model, using=self._db)

    def by_likes(self):
        return self.by_likes()

    def by_dislikes(self):
        return self.by_dislikes()

    def by_author(self, author: CustomUser):
        return self.get_queryset().by_author(author)

    def by_published_date(self):
        return self.get_queryset().by_published_date()
