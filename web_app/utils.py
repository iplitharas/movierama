"""Helper function for the web-app endpoints"""
import logging
from dataclasses import dataclass
from typing import List

from django.http import HttpRequest

from accounts.models import CustomUser
from movies.models import Movie
from movies.movie_manager import MovieQuerySet

logger = logging.getLogger(__name__)


@dataclass
class TemplateData:
    movie: Movie = None
    allow_edit: bool = False
    allow_delete: bool = False
    allow_like: bool = False
    allow_dislike: bool = False


def apply_queryset_filtering(
    request: HttpRequest, queryset: MovieQuerySet
) -> MovieQuerySet:
    """Apply user filtering based on the user requests"""
    movies = queryset.all().order_by("id")
    if request.GET.get("filter") == "date":
        movies = queryset.all().order_by("created_date")

    if request.GET.get("filter") == "released_date":
        movies = queryset.by_published_date()
        logger.debug("Filter by `released_date movies` %s" % movies)

    if request.GET.get("filter") == "likes":
        movies = queryset.by_likes()
        logger.debug("Filter by `likes` %s" % movies)

    if request.GET.get("filter") == "dislikes":
        movies = queryset.by_dislikes()
        logger.debug("Filter by `dislikes` %s" % movies)

    if request.GET.get("filter") == "by_current_user":
        movies = queryset.by_author(author=request.user)
        logger.debug("Filter `by_current_user` %s movies %s" % (request.user, movies))

    if request.GET.get("author"):
        author_id = request.GET.get("author")
        movies = queryset.by_author(author=CustomUser.objects.get(id=author_id))
        logger.debug("Filter by `author` with id: %s movies %s" % (author_id, movies))
    return movies


def get_template_data(movies: MovieQuerySet, user: CustomUser) -> List[TemplateData]:
    """
    Helper function for determining if a user can `like/dislike` or
    `edit/delete` a movie
    """
    data = []
    for movie in movies:
        temp_data = TemplateData()
        temp_data.movie = movie
        data.append(temp_data)
        # author users can't like their own movie reviews
        if movie.author.id == user.id:
            # users can't add reaction on their movie reviews
            temp_data.allow_edit = True
            temp_data.allow_delete = True
            # like/dislike
            temp_data.allow_like = None
            temp_data.allow_dislike = None
        # user has already liked the movie
        elif user in movie.likes.all():
            temp_data.allow_like = False
            temp_data.allow_dislike = True
        # user has already dis-liked the movie
        elif user in movie.dislikes.all():
            temp_data.allow_like = True
            temp_data.allow_dislike = False
        else:
            # user hasn't liked or dislike the movie
            temp_data.allow_like = True
            temp_data.allow_dislike = True
    return data
