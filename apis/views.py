from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from music.models import Song
from .serializers import SongSerializer


from rest_framework import filters

class SongAPIListView(generics.ListCreateAPIView):
    """
    GET  /api/songs/ — Lista paginata di tutti i brani (pubblico).
    POST /api/songs/ — Crea un nuovo brano (solo utenti autenticati).
    Supporta filtraggio per artist e genre via query params.
    Supporta ricerca testuale via ?search=...
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['artist', 'genre']
    search_fields = ['title', 'artist']


class SongAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/songs/<pk>/ — Dettaglio brano (pubblico).
    PUT    /api/songs/<pk>/ — Aggiorna brano completo (autenticato).
    PATCH  /api/songs/<pk>/ — Aggiorna parzialmente (autenticato).
    DELETE /api/songs/<pk>/ — Elimina brano (autenticato).
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
