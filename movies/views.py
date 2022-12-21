from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.views.generic import ListView
from .models import Movie
from .serializers import MovieSerializer
from rest_framework import generics
from .persmissions import IsAuthorOrReadOnly


class MovieListView(ListView):
    model = Movie
    template_name = "movies_list.html"


class MovieAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class MoveAPICreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieListAPIList(generics.ListAPIView):
    # permission_classes = permissions.IsAuthenticated
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # @action(methods=["POST"], detail=True)
    # def post(self, request, format=None):
    #     serializer = MovieSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # @action(methods=["GET"], detail=True)
    # def get_movie(self, request, **kwargs):
    #     pass


