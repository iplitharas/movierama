

from movies.models import Movie
from .serializers import MovieSerializer
from rest_framework import generics
from movies.persmissions import IsAuthorOrReadOnly


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


