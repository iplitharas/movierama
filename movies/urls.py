from django.urls import path

from .views import MovieList


urlpatterns = [
    path("api/movies/v1", MovieList.as_view()),
]