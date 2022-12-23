from django.urls import path

from .views import (
    HomePageView,
    delete_movie,
    dislike_movie,
    like_movie,
    new_movie,
    update_movie,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("add_movie/", new_movie, name="new-movie"),
    path("update_movie/<int:id>/", update_movie, name="update-movie"),
    path("delete_movie/<int:id>/", delete_movie, name="delete-movie"),
    path("like_movie/<int:id>/", like_movie, name="like-movie"),
    path("dislike_movie/<int:id>/", dislike_movie, name="dislike-movie"),
]
