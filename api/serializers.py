"""Api serializers"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["title", "desc", "genre", "year", "likes", "dislikes", "id"]
        read_only_fields = (
            "id",
            "created_date",
            "updated_date",
            "likes",
            "dislikes",
        )


class MovieAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["title", "desc", "genre", "year", "likes", "dislikes", "id"]
        read_only_fields = (
            "id",
            "created_date",
            "updated_date",
            "likes",
            "dislikes",
        )

    def create(self, *args, **kwargs):
        user_id = self.context.get("user_id")
        if self.is_valid():
            User = get_user_model()
            user = get_object_or_404(User, id=user_id)
            movie = Movie.objects.create(**self.validated_data, author=user)
            return movie
