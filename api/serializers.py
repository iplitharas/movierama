from rest_framework import serializers

from movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["title", "desc", "genre", "year", "author", "likes", "dislikes", "id"]
        read_only_fields = (
            "id",
            "created_date",
            "updated_date",
            "likes",
            "dislikes",
            "id",
        )
