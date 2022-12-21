from django.urls import path

from .views import HomePageView, new_movie

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("add_movie/", new_movie, name="new-movie")
]
