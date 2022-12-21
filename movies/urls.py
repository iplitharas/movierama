from django.urls import path

from .views import MovieListView, MovieListAPIList, MovieAPIDetailView, MoveAPICreateView

urlpatterns = [
    path("api/movies/v1/", MovieListAPIList.as_view()),
    path("api/movies/v1/<int:pk>", MovieAPIDetailView.as_view()),
    path("api/movies/v1/new", MoveAPICreateView.as_view()),
    path("", MovieListView.as_view()),
]
