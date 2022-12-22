from django.urls import path, re_path

from .views import HomePageView, new_movie, update_movie, delete_movie

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("add_movie/", new_movie, name="new-movie"),
    path("update_movie/<int:id>/", update_movie, name="update-movie"),
    path("delete_movie/<int:id>/", delete_movie, name="delete-movie")
]
