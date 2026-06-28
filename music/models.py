from django.conf import settings
from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='songs',
    )
    duration = models.DurationField()
    audio_file = models.FileField(
        upload_to='songs/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'])]
    )
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_songs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def get_absolute_url(self):
        return reverse('music:song_list')


class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.song.title}"

    class Meta:
        ordering = ['-created_at']


class Playlist(models.Model):
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
    is_editorial = models.BooleanField(default=False)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_playlists',
        blank=True
    )

    def __str__(self):
        return f'{self.name} ({self.owner})'

    def get_absolute_url(self):
        return reverse('music:playlist_list')
