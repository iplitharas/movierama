from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "genre",
        "year",
        "created_date",
        "updated_date",
        "likes",
        "dislikes",
    )
    list_display = (
        "title",
        "genre",
        "year",
        "created_date",
        "updated_date",
        "likes",
        "dislikes",
    )
    readonly_fields = (
        "created_date",
        "updated_date",
    )
