from django.shortcuts import render, redirect
from django.views import generic
from movies.models import Movie
from .forms import MovieForm


class HomePageView(generic.ListView):
    template_name = "movies/home.html"
    model = Movie
    # context_object_name = "movies-list"
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HomePageView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context["movies"] = self.queryset.all()
        return context

    def get_queryset(self):
        return Movie.objects.all()


def new_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST, author=request.user)
        if form.is_valid():
            Movie.objects.create(
                author=form.author,
                title=form.cleaned_data["title"],
                desc=form.cleaned_data["desc"],
                genre=form.cleaned_data["genre"],
                year=form.cleaned_data["year"],
            )
            return redirect("home")

    form = MovieForm()
    return render(
        request=request, template_name="movies/new.html", context={"form": form}
    )
