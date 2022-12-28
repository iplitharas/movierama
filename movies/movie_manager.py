"""Movie model custom ManagerQuerySet"""
from django.db import models
from django.db.models import Count

from accounts.models import CustomUser


class MovieQuerySet(models.QuerySet):
    """MovieQuerySet"""

    def by_author(self, author: CustomUser):
        """Returns movies filtered by author"""
        return self.filter(author=author)

    def by_published_date(self):
        """Returns movies ordered by year"""
        return self.order_by("year")

    def by_likes(self):
        """Returns movies ordered by likes"""
        return self.annotate(tmp=Count("likes")).order_by("-tmp")

    def by_dislikes(self):
        """Returns movies ordered by dislikes"""
        # by default the order is ascending
        # `-` reverse that
        return self.annotate(tmp=Count("dislikes")).order_by("-tmp")


class MovieManager(models.Manager):
    """Movie Manager"""

    def get_queryset(self):
        """return the default QuerySet"""
        return MovieQuerySet(self.model, using=self._db)

    def by_likes(self):
        """Returns movies ordered by likes"""
        return self.get_queryset().by_likes()

    def by_dislikes(self):
        """Returns movies ordered by dislikes"""
        return self.get_queryset().by_dislikes()

    def by_author(self, author: CustomUser):
        """Returns movies filtered by author"""
        return self.get_queryset().by_author(author)

    def by_published_date(self):
        """Returns movies ordered by likes"""
        return self.get_queryset().by_published_date()
