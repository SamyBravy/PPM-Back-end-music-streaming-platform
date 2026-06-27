from django.urls import path

from .views import (
    SongListView,
    SongDetailView,
    SongCreateView,
    SongUpdateView,
    SongDeleteView,
    PlaylistListView,
    PlaylistDetailView,
    PlaylistCreateView,
    PlaylistUpdateView,
    PlaylistDeleteView,
    CommentDeleteView,
    add_song_to_playlist,
    remove_song_from_playlist,
    GenreListView,
    GenreCreateView,
    GenreUpdateView,
    GenreDeleteView,
    toggle_favorite_playlist,
    toggle_like_song,
    toggle_like_comment,
)

app_name = 'music'

urlpatterns = [
    path('comments/<int:pk>/like/', toggle_like_comment, name='toggle_like_comment'),
    path('songs/', SongListView.as_view(), name='song_list'),
    path('songs/<int:pk>/', SongDetailView.as_view(), name='song_detail'),
    path('songs/add/', SongCreateView.as_view(), name='song_create'),
    path('songs/<int:pk>/edit/', SongUpdateView.as_view(), name='song_update'),
    path('songs/<int:pk>/delete/', SongDeleteView.as_view(), name='song_delete'),
    path('songs/<int:pk>/like/', toggle_like_song, name='toggle_like_song'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('songs/<int:song_id>/add-to-playlist/<int:playlist_id>/', add_song_to_playlist, name='add_to_playlist'),
    path('songs/<int:song_id>/remove-from-playlist/<int:playlist_id>/', remove_song_from_playlist, name='remove_from_playlist'),
    path('playlists/', PlaylistListView.as_view(), name='playlist_list'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlists/add/', PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlists/<int:pk>/edit/', PlaylistUpdateView.as_view(), name='playlist_update'),
    path('playlists/<int:pk>/delete/', PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('playlists/<int:pk>/favorite/', toggle_favorite_playlist, name='toggle_favorite_playlist'),
    
    # Genre Management (Curator only)
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/add/', GenreCreateView.as_view(), name='genre_create'),
    path('genres/<int:pk>/edit/', GenreUpdateView.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', GenreDeleteView.as_view(), name='genre_delete'),
]
