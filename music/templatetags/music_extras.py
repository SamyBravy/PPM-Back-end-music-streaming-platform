from django import template

register = template.Library()

@register.filter
def has_song(playlist, song):
    """Restituisce True se la canzone è nella playlist."""
    return playlist.songs.filter(id=song.id).exists()

@register.filter
def available_playlists(user, song):
    """Restituisce le playlist dell'utente che non contengono ancora la canzone."""
    if not user.is_authenticated:
        return []
    return user.playlists.exclude(songs=song)
