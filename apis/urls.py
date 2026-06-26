from django.urls import path

from .views import SongAPIListView, SongAPIDetailView

app_name = 'apis'

urlpatterns = [
    path('songs/', SongAPIListView.as_view(), name='song_api_list'),
    path('songs/<int:pk>/', SongAPIDetailView.as_view(), name='song_api_detail'),
]
