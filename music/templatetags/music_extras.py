from django import template

register = template.Library()

@register.filter
def has_song(playlist, song):
    return playlist.songs.filter(id=song.id).exists()

@register.filter
def available_playlists(user, song):
    if not user.is_authenticated:
        return []
    return user.playlists.exclude(songs=song)
