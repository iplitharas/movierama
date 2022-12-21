from django.urls import path

from .views import MovieListAPIList, MovieAPIDetailView, MoveAPICreateView

urlpatterns = [
    path("movies/v1/", MovieListAPIList.as_view()),
    path("movies/v1/<int:pk>", MovieAPIDetailView.as_view()),
    path("movies/v1/new", MoveAPICreateView.as_view()),
]
