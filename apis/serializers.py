from rest_framework import serializers

from music.models import Song


class SongSerializer(serializers.ModelSerializer):
    """Serializzatore per il modello Song — converte i queryset in JSON."""
    genre = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'genre', 'duration', 'created_at']
