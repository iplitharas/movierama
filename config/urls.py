"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Movierama API",
        description="API for movies",
        default_version="v1",
        contact=openapi.Contact(email="johnplitharas@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

from .views import FacebookLogin, GithubLogin

urlpatterns = [
    path("admin/", admin.site.urls),
    # use build-in django auth urls
    path("", include("web_app.urls")),
    path("api/", include("api.urls")),
    path("accounts/", include("accounts.urls")),
    # Adds login/logout at rest-framework page
    path("api-auth/", include("rest_framework.urls")),
    # add login/logout from dj-rest-auth
    path("api/v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    # add registration from django-allauth
    path(
        "api/v1/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")
    ),
    path("api/v1/dj-rest-auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("api/v1/dj-rest-auth/github/", GithubLogin.as_view(), name="github_login"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
