from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie
from movies.persmissions import IsAuthorOrReadOnly

from .serializers import MovieAddSerializer, MovieSerializer


class MovieAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class MoveAPICreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieAddSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user_id": self.request.user.id})
        return context


class MovieListAPIList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
