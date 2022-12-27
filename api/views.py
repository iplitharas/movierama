from rest_framework import generics

from movies.models import Movie
from movies.persmissions import IsAuthorOrReadOnly

from .serializers import MovieSerializer


class MovieAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class MoveAPICreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieListAPIList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
