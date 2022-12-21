from django.db import models


class MovieManager(models.Manager):

    def get_queryset(self):
        return super(MovieManager,self).get_queryset()

    def by_likes(self):
        pass
