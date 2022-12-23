"""
Web-app views using the `Movie` model for:
1) listing all the existing movie reviews: `HomePageView`
2) creating a new movie review: `new_movie`
3) updating a movie review: `update_movie`
4) deleting a movie review: `delete_movie`
5) add likes to a movie review: `like_movie`
6) add dislikes to a movie review: `dislike_movie`
"""
import logging
from dataclasses import dataclass

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from accounts.models import CustomUser
from movies.models import Movie
from movies.persmissions import IsAuthorOrReadOnly

from .forms import MovieForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


@dataclass
class TemplateData:
    movie: Movie = None
    allow_edit: bool = False
    allow_delete: bool = False
    allow_like: bool = False
    allow_dislike: bool = False


class HomePageView(generic.ListView):
    """
    Class based view for listing all movie reviews.
    """

    template_name = "movies/home.html"
    model = Movie
    # context_object_name = "movies-list"
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        """
        Allows custom filtering on the queryset.
        """
        context = super().get_context_data(**kwargs)
        # First, specify the movies query set
        movies = self.queryset.all().order_by("id")

        if self.request.GET.get("filter") == "date":

            movies = self.queryset.all().order_by("created_date")

        if self.request.GET.get("filter") == "released_date":
            movies = self.queryset.by_published_date()
            logger.debug("Filter by `released_date movies` %s" % movies)

        if self.request.GET.get("filter") == "likes":
            movies = self.queryset.by_likes()
            logger.debug("Filter by `likes` %s" % movies)

        if self.request.GET.get("filter") == "dislikes":
            movies = self.queryset.by_dislikes()
            logger.debug("Filter by `dislikes` %s" % movies)

        if self.request.GET.get("filter") == "by_current_user":
            movies = self.queryset.by_author(author=self.request.user)
            logger.debug(
                "Filter `by_current_user` %s movies %s" % (self.request.user, movies)
            )

        if self.request.GET.get("author"):
            author_id = self.request.GET.get("author")
            movies = self.queryset.by_author(
                author=CustomUser.objects.get(id=author_id)
            )
            logger.debug(
                "Filter by `author` with id: %s movies %s" % (author_id, movies)
            )

        data = []
        for movie in movies:
            temp_data = TemplateData()
            temp_data.movie = movie
            data.append(temp_data)
            # author users can't like their own movie reviews
            if movie.author.id == self.request.user.id:
                # users can't add reaction on their movie reviws
                temp_data.allow_edit = True
                temp_data.allow_delete = True
                # like/dislike
                temp_data.allow_like = None
                temp_data.allow_dislike = None
            # user has already liked the movie
            elif self.request.user in movie.likes.all():
                temp_data.allow_like = False
                temp_data.allow_dislike = True
            # user has already dis-liked the movie
            elif self.request.user in movie.dislikes.all():
                temp_data.allow_like = True
                temp_data.allow_dislike = False
            else:
                # user hasn't liked or dislike the movie
                temp_data.allow_like = True
                temp_data.allow_dislike = True
        context["data"] = data
        return context


@login_required(login_url="/accounts/login/")
def new_movie(request: HttpRequest) -> HttpResponse:
    """
    Function handler for creating a new movie review.
    """
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, author=request.user)
        if form.is_valid():
            Movie.objects.create(
                author=form.author,
                title=form.cleaned_data["title"],
                desc=form.cleaned_data["desc"],
                genre=form.cleaned_data["genre"],
                year=form.cleaned_data["year"],
                cover=request.FILES["cover"],
            )
            logger.info("Successfully created the movie")
            return redirect("home")

    form = MovieForm()
    return render(
        request=request, template_name="movies/new.html", context={"form": form}
    )


# pylint: disable=redefined-builtin,invalid-name
@login_required(login_url="/accounts/login/")
def update_movie(request: HttpRequest, id: int) -> HttpResponse:
    """
    Function handler for updating a movie review.
    """
    movie = get_object_or_404(Movie, id=id)
    if request.user != movie.author:
        return HttpResponse("Unauthorized", status=401)
    if request.method == "POST":
        form = MovieForm(
            request.POST, request.FILES, author=request.user, instance=movie
        )
        if form.is_valid():
            Movie.objects.filter(id=movie.id).update(
                author=form.author,
                title=form.cleaned_data["title"],
                desc=form.cleaned_data["desc"],
                genre=form.cleaned_data["genre"],
                year=form.cleaned_data["year"],
            )
            if request.FILES.get("cover"):
                movie = Movie.objects.get(id=movie.id)
                movie.cover = request.FILES["cover"]
                movie.save()
        logger.info("Successfully updated the movie")
        return redirect("home")

    form = MovieForm(instance=movie)
    return render(
        request=request,
        template_name="movies/edit.html",
        context={"form": form, "id": id},
    )


# pylint: disable=redefined-builtin,invalid-name
@login_required(login_url="/accounts/login/")
def delete_movie(request: HttpRequest, id: int) -> HttpResponse:
    """
    Function handler for deleting a movie review.
    """
    context = {"id": id}
    obj = get_object_or_404(Movie, id=id)
    if request.user != obj.author:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        obj.delete()
        logger.info("Successfully deleted the movie")
        return redirect("home")

    return render(request, "movies/delete.html", context)


@login_required(login_url="/accounts/login/")
def like_movie(request: HttpRequest, id: int) -> HttpResponse:
    """
    Like function view for handling likes from users for one movie.
    """
    movie = get_object_or_404(Movie, id=id)

    if request.method == "POST":
        user = CustomUser.objects.filter(pk=request.user.id)
        if user.exists():
            # Many-to-Many it's a set
            # user liked this movie review
            # revert it
            if user.first() in movie.likes.all():
                movie.likes.remove(user.first())
                logger.info(
                    "Reverted like from user: %s for movie %s"
                    % (request.user.id, movie.id),
                )
                return redirect("home")

            if user.first() not in movie.likes.all():
                movie.likes.add(user.first())
                logger.info(
                    "Added a like from user: %s to movie %s"
                    % (request.user.id, movie.id),
                )
            if user.first() in movie.dislikes.all():
                movie.dislikes.remove(user.first())
                logger.info(
                    "User %s likes movie %s, deleted the dislike"
                    % (request.user.id, movie.id),
                )
            movie.save()
    # go to home page in any case
    return redirect("home")


@login_required(login_url="/accounts/login/")
def dislike_movie(request: HttpRequest, id: int) -> HttpResponse:
    """
    Dislike function view for handling dislikes from users for one movie.
    """
    movie = get_object_or_404(Movie, id=id)
    if request.method == "POST":
        user = CustomUser.objects.filter(pk=request.user.id)
        if user.exists():
            if user.first() in movie.dislikes.all():
                logger.info(
                    "Reverted dislike from user: %s for movie %s"
                    % (request.user.id, movie.id),
                )
                movie.dislikes.remove(user.first())
                return redirect("home")

            if user.first() not in movie.dislikes.all():
                logger.info(
                    "Added a dislike from user: %s to movie %s"
                    % (request.user.id, movie.id),
                )
                movie.dislikes.add(user.first())

            if user.first() in movie.likes.all():
                movie.likes.remove(user.first())
                logger.info(
                    "User %s dislike movie %s, deleted the like"
                    % (request.user.id, movie.id),
                )
            movie.save()
    # go to home page in any case
    return redirect("home")
