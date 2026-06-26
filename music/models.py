from django.conf import settings
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    """Genere musicale (es. Rock, Jazz, Pop)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    """Singolo brano musicale, associato a un genere (One-to-Many)."""
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='songs',
    )
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def get_absolute_url(self):
        return reverse('music:song_list')


class Comment(models.Model):
    """Commento inserito da un utente sotto un brano specifico."""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.song.title}"

    class Meta:
        ordering = ['-created_at']


class Playlist(models.Model):
    """Playlist creata da un utente, contiene brani (Many-to-Many)."""
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='playlists',
    )
    songs = models.ManyToManyField(
        Song,
        related_name='playlists',
        blank=True,
    )
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.owner})'

    def get_absolute_url(self):
        return reverse('music:playlist_list')
