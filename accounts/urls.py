from django.urls import path, include
from .views import SignUpPageView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", SignUpPageView.as_view(), name="signup"),
]
