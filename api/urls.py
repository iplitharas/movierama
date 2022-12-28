from django.urls import path

from .views import MoveAPICreateView, MovieAPIDetailView, MovieListAPIList

urlpatterns = [
    path("movies/v1/", MovieListAPIList.as_view(), name="movies"),
    path("movies/v1/<int:pk>", MovieAPIDetailView.as_view()),
    path("movies/v1/new", MoveAPICreateView.as_view(), name="movies-new"),
]
