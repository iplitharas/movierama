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

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from accounts.models import CustomUser
from movies.models import Movie

from .forms import MovieForm
from .utils import apply_queryset_filtering, get_template_data

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
        Specify the `context/template` data based on
        custom filter and if users can `edit/delete`
        or `like/dislike` a movie.
        """
        context = super().get_context_data(**kwargs)
        # First, specify the movies query set
        movies = apply_queryset_filtering(request=self.request, queryset=self.queryset)
        context["data"] = get_template_data(movies, self.request.user)
        return context


@login_required(login_url="/accounts/login/")
def new_movie(request: HttpRequest) -> HttpResponse:
    """
    Function handler for creating a new movie review.
    """
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, author=request.user)
        if form.is_valid():

            movie = Movie.objects.create(
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
            logger.info("Successfully created the movie")
            return redirect("home")

        logger.info("Cannot create a new movie due to: %s" % form.errors)
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

        logger.info("Cannot update a new movie due to: %s" % form.errors)
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

    if request.user == movie.author:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        user = CustomUser.objects.filter(pk=request.user.id)
        if user.exists():
            user = user.first()
            # Many-to-Many it's a set
            # user liked this movie review
            # revert it
            if user in movie.likes.all():
                movie.likes.remove(user)
                logger.info(
                    "Revert like from user: %s for movie %s"
                    % (request.user.id, movie.id),
                )
                return redirect("home")

            if user not in movie.likes.all():
                movie.likes.add(user)
                logger.info(
                    "Added a like from user: %s to movie %s"
                    % (request.user.id, movie.id),
                )
            if user in movie.dislikes.all():
                movie.dislikes.remove(user)
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

    if request.user == movie.author:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        user = CustomUser.objects.filter(pk=request.user.id)
        if user.exists():
            user = user.first()
            if user in movie.dislikes.all():
                logger.info(
                    "Reverted dislike from user: %s for movie %s"
                    % (request.user.id, movie.id),
                )
                movie.dislikes.remove(user)
                return redirect("home")

            if user not in movie.dislikes.all():
                logger.info(
                    "Added a dislike from user: %s to movie %s"
                    % (request.user.id, movie.id),
                )
                movie.dislikes.add(user)

            if user in movie.likes.all():
                movie.likes.remove(user)
                logger.info(
                    "User %s dislike movie %s, deleted the like"
                    % (request.user.id, movie.id),
                )
            movie.save()
    # go to home page in any case
    return redirect("home")
