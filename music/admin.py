from django.contrib import admin

from .models import Genre, Song, Playlist, Comment


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'duration', 'created_at']
    list_filter = ['genre', 'created_at']
    search_fields = ['title', 'artist']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    list_filter = ['owner']
    search_fields = ['name']
    filter_horizontal = ['songs']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'song', 'created_at', 'text']
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username']
