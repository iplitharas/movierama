"""
Web app views using the `Movie` model for
1) listing all the existing movie reviews: `HomePageView`
2) creating a new movie review: `new_movie`
3) updating a movie review: `update_movie`
4) deleting a movie review: `delete_movie`
"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from movies.models import Movie
from .forms import MovieForm


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
        if self.request.GET.get("filter") == "date":
            context["movies"] = self.queryset.all().order_by("created_date")
            return context
        if self.request.GET.get("filter") == "published_date":
            context["movies"] = self.queryset.all().order_by("year")
            return context
        if self.request.GET.get("filter") == "by_user":
            context["movies"] = self.queryset.all().filter(author=self.request.user)
            return context

        context["movies"] = self.queryset.all().order_by("id")
        return context


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
            return redirect("home")

    form = MovieForm()
    return render(
        request=request, template_name="movies/new.html", context={"form": form}
    )


# pylint: disable=redefined-builtin,invalid-name
def update_movie(request: HttpRequest, id: int) -> HttpResponse:
    """
    Function handler for updating a movie review.
    """
    instance = get_object_or_404(Movie, id=id)
    if request.method == "POST":
        form = MovieForm(
            request.POST, request.FILES, author=request.user, instance=instance
        )
        if form.is_valid():
            Movie.objects.filter(id=instance.id).update(
                author=form.author,
                title=form.cleaned_data["title"],
                desc=form.cleaned_data["desc"],
                genre=form.cleaned_data["genre"],
                year=form.cleaned_data["year"],
            )
            if request.FILES["cover"]:
                movie = Movie.objects.get(id=instance.id)
                movie.cover = request.FILES["cover"]
                movie.save()

        return redirect("home")

    form = MovieForm(instance=instance)
    return render(
        request=request,
        template_name="movies/edit.html",
        context={"form": form, "id": id},
    )


# pylint: disable=redefined-builtin,invalid-name
def delete_movie(request: HttpRequest, id: int) -> HttpResponse:
    """
    Function handler for deleting a movie review.
    """
    context = {"id": id}
    # fetch the object related to passed id
    obj = get_object_or_404(Movie, id=id)

    if request.method == "POST":
        obj.delete()

        return redirect("home")

    return render(request, "movies/delete.html", context)
