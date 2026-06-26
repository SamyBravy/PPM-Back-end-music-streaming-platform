import os
import django
from datetime import timedelta

# Configura l'ambiente Django per poter eseguire script standalone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from django.contrib.auth import get_user_model
from music.models import Genre, Song

User = get_user_model()

def seed():
    print("Inizio popolamento del database...")

    # 1. Accounts
    print("-> Creazione account demo...")
    if not User.objects.filter(username='admin_demo').exists():
        User.objects.create_superuser('admin_demo', 'admin@example.com', 'admin12345')
        print("   Account admin_demo creato.")
    
    if not User.objects.filter(username='curator_demo').exists():
        User.objects.create_user('curator_demo', 'curator@example.com', 'curator12345', role='curator', is_staff=True)
        print("   Account curator_demo creato.")

    if not User.objects.filter(username='listener_demo').exists():
        User.objects.create_user('listener_demo', 'listener@example.com', 'listener12345', role='listener')
        print("   Account listener_demo creato.")

    # 2. Genres
    print("-> Creazione generi musicali...")
    genres_data = ['Rock', 'Jazz', 'Pop', 'Electronic']
    genres = {}
    for g in genres_data:
        genre, created = Genre.objects.get_or_create(name=g)
        genres[g] = genre
        if created:
            print(f"   Genere {g} creato.")

    # 3. Songs
    print("-> Creazione canzoni...")
    songs_data = [
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "genre": genres['Rock'], "duration": timedelta(minutes=8, seconds=2)},
        {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": genres['Rock'], "duration": timedelta(minutes=5, seconds=55)},
        {"title": "Hotel California", "artist": "Eagles", "genre": genres['Rock'], "duration": timedelta(minutes=6, seconds=30)},
        {"title": "Take Five", "artist": "Dave Brubeck", "genre": genres['Jazz'], "duration": timedelta(minutes=5, seconds=24)},
        {"title": "So What", "artist": "Miles Davis", "genre": genres['Jazz'], "duration": timedelta(minutes=9, seconds=22)},
        {"title": "My Favorite Things", "artist": "John Coltrane", "genre": genres['Jazz'], "duration": timedelta(minutes=13, seconds=41)},
        {"title": "Billie Jean", "artist": "Michael Jackson", "genre": genres['Pop'], "duration": timedelta(minutes=4, seconds=54)},
        {"title": "Shape of You", "artist": "Ed Sheeran", "genre": genres['Pop'], "duration": timedelta(minutes=3, seconds=53)},
        {"title": "Blinding Lights", "artist": "The Weeknd", "genre": genres['Pop'], "duration": timedelta(minutes=3, seconds=20)},
        {"title": "Strobe", "artist": "deadmau5", "genre": genres['Electronic'], "duration": timedelta(minutes=10, seconds=37)},
        {"title": "One More Time", "artist": "Daft Punk", "genre": genres['Electronic'], "duration": timedelta(minutes=5, seconds=20)},
        {"title": "Animals", "artist": "Martin Garrix", "genre": genres['Electronic'], "duration": timedelta(minutes=5, seconds=4)},
    ]

    for data in songs_data:
        song, created = Song.objects.get_or_create(title=data['title'], artist=data['artist'], defaults={'genre': data['genre'], 'duration': data['duration']})
        if created:
            print(f"   Canzone '{song.title}' di {song.artist} creata.")

    print("Popolamento del database completato con successo!")

if __name__ == '__main__':
    seed()
