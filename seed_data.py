import os
import django
from datetime import timedelta
import random

# Configura l'ambiente Django per poter eseguire script standalone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from django.contrib.auth import get_user_model
from music.models import Genre, Song, Playlist, Comment
from users.models import FriendRequest

User = get_user_model()

def seed():
    print("Inizio popolamento del database...")

    # 1. Accounts
    print("-> Creazione account demo...")
    users = {}
    
    admin, _ = User.objects.get_or_create(username='admin_demo', defaults={
        'email': 'admin@example.com',
        'role': 'curator',
        'is_staff': True,
        'is_superuser': True,
        'profile_icon': '🐯'
    })
    admin.set_password('admin12345')
    admin.save()
    users['admin'] = admin
    print("   Account admin_demo creato.")
    
    curator, _ = User.objects.get_or_create(username='curator_demo', defaults={
        'email': 'curator@example.com',
        'role': 'curator',
        'is_staff': False,
        'profile_icon': '🦊'
    })
    curator.set_password('curator12345')
    curator.save()
    users['curator'] = curator
    print("   Account curator_demo creato.")

    moderator, _ = User.objects.get_or_create(username='moderator_demo', defaults={
        'email': 'moderator@example.com',
        'role': 'moderator',
        'is_staff': False,
        'profile_icon': '👽'
    })
    moderator.set_password('moderator12345')
    moderator.save()
    users['moderator'] = moderator
    print("   Account moderator_demo creato.")

    listener, _ = User.objects.get_or_create(username='listener_demo', defaults={
        'email': 'listener@example.com',
        'role': 'listener',
        'profile_icon': '🎧'
    })
    listener.set_password('listener12345')
    listener.save()
    users['listener'] = listener
    print("   Account listener_demo creato.")
    
    # Utenti aggiuntivi per testare le amicizie
    alice, _ = User.objects.get_or_create(username='alice', defaults={'email': 'alice@example.com', 'role': 'listener', 'profile_icon': '🐱'})
    alice.set_password('password123')
    alice.save()
    users['alice'] = alice

    bob, _ = User.objects.get_or_create(username='bob', defaults={'email': 'bob@example.com', 'role': 'listener', 'profile_icon': '🐶'})
    bob.set_password('password123')
    bob.save()
    users['bob'] = bob

    # 2. Amicizie
    print("-> Configurazione amicizie e richieste...")
    # Listener e Alice sono amici
    listener.friends.add(alice)
    # Alice ha inviato una richiesta a Bob
    FriendRequest.objects.get_or_create(sender=alice, receiver=bob)
    # Bob ha inviato una richiesta a Listener
    FriendRequest.objects.get_or_create(sender=bob, receiver=listener)

    # 3. Genres
    print("-> Creazione generi musicali...")
    genres_data = ['Rock', 'Jazz', 'Pop', 'Electronic', 'Classical']
    genres = {}
    for g in genres_data:
        genre, created = Genre.objects.get_or_create(name=g, defaults={'description': f'This is the {g} genre.'})
        genres[g] = genre
        if created:
            print(f"   Genere {g} creato.")

    # 4. Songs
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

    all_songs = []
    for data in songs_data:
        song, created = Song.objects.get_or_create(title=data['title'], artist=data['artist'], defaults={'genre': data['genre'], 'duration': data['duration']})
        all_songs.append(song)
        if created:
            print(f"   Canzone '{song.title}' di {song.artist} creata.")

    # 5. Mi Piace (Like alle canzoni)
    print("-> Aggiunta like alle canzoni...")
    for song in all_songs:
        # Aggiungiamo like casuali
        likers = random.sample(list(users.values()), k=random.randint(0, 3))
        for liker in likers:
            song.likes.add(liker)

    # 6. Playlists
    print("-> Creazione playlist...")
    # Playlist Editoriale
    editorial_pl, _ = Playlist.objects.get_or_create(
        name="Top Hits", owner=curator, defaults={'is_public': True, 'is_editorial': True}
    )
    editorial_pl.songs.set(all_songs[:5])

    # Playlist Pubblica di Listener
    public_pl, _ = Playlist.objects.get_or_create(
        name="My Chill Vibes", owner=listener, defaults={'is_public': True}
    )
    public_pl.songs.set(all_songs[4:8])

    # Playlist Privata di Listener
    private_pl, _ = Playlist.objects.get_or_create(
        name="Secret Guilty Pleasures", owner=listener, defaults={'is_public': False}
    )
    private_pl.songs.set(all_songs[8:10])
    
    # Follower Playlist
    editorial_pl.followers.add(listener, alice)
    public_pl.followers.add(bob)

    # 7. Commenti
    print("-> Aggiunta commenti...")
    song_to_comment = all_songs[1] # Bohemian Rhapsody
    if not Comment.objects.filter(song=song_to_comment, author=listener).exists():
        c1 = Comment.objects.create(song=song_to_comment, author=listener, text="This is a masterpiece!")
        Comment.objects.create(song=song_to_comment, author=curator, text="I totally agree.", parent=c1)
        Comment.objects.create(song=song_to_comment, author=alice, text="Timeless classic.")

    print("Popolamento del database completato con successo!")

if __name__ == '__main__':
    seed()
