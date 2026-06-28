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
    print("Inizio popolamento massivo del database...")

    # 1. Accounts (creazione di svariati utenti con ruoli diversi)
    print("-> Creazione account...")
    users = {}
    
    # Staff / Curators / Moderators
    accounts = [
        ('admin_demo', 'admin@example.com', 'curator', True, '🐯', 'admin12345'),
        ('curator_demo', 'curator@example.com', 'curator', False, '🦊', 'curator12345'),
        ('moderator_demo', 'moderator@example.com', 'moderator', False, '👽', 'moderator12345'),
        ('sara_curates', 'sara@example.com', 'curator', False, '🤖', 'password123'),
        ('mike_curates', 'mike@example.com', 'curator', False, '🤠', 'password123'),
        ('john_mod', 'john@example.com', 'moderator', False, '👻', 'password123'),
        ('lisa_mod', 'lisa@example.com', 'moderator', False, '👤', 'password123'),
    ]
    
    for username, email, role, is_super, icon, pwd in accounts:
        user, _ = User.objects.get_or_create(username=username, defaults={
            'email': email, 'role': role, 'is_staff': is_super, 'is_superuser': is_super, 'profile_icon': icon
        })
        user.set_password(pwd)
        user.save()
        users[username] = user
        
    # Listeners
    listeners = [
        ('listener_demo', 'listener@example.com', '👤', 'listener12345'),
        ('alice', 'alice@test.com', '🐱', 'password123'),
        ('bob', 'bob@test.com', '🐶', 'password123'),
        ('charlie', 'charlie@test.com', '🐸', 'password123'),
        ('dave', 'dave@test.com', '🐼', 'password123'),
        ('eve', 'eve@test.com', '🐰', 'password123'),
        ('frank', 'frank@test.com', '🦁', 'password123'),
        ('spambot', 'spam@test.com', '🤖', 'password123')
    ]
    for username, email, icon, pwd in listeners:
        user, _ = User.objects.get_or_create(username=username, defaults={'email': email, 'role': 'listener', 'profile_icon': icon})
        user.set_password(pwd)
        user.save()
        users[username] = user

    # 2. Amicizie
    print("-> Configurazione sistema di amicizie e richieste...")
    # Alice è amica di Bob e Charlie
    users['alice'].friends.add(users['bob'], users['charlie'])
    # Dave invia richiesta ad Alice
    FriendRequest.objects.get_or_create(sender=users['dave'], receiver=users['alice'])
    # Eve invia richiesta ad Alice
    FriendRequest.objects.get_or_create(sender=users['eve'], receiver=users['alice'])
    # Alice invia richiesta a Frank
    FriendRequest.objects.get_or_create(sender=users['alice'], receiver=users['frank'])

    # 3. Genres
    print("-> Creazione generi musicali espansi...")
    genres_data = ['Rock', 'Jazz', 'Pop', 'Electronic', 'Classical', 'Hip Hop', 'Indie', 'Metal', 'Lo-Fi']
    genres = {}
    for g in genres_data:
        genre, _ = Genre.objects.get_or_create(name=g, defaults={'description': f'Explore the best of {g}.'})
        genres[g] = genre

    # 4. Songs (Molte più canzoni, alcune con audio collegato)
    print("-> Creazione catalogo musicale...")
    songs_data = [
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "genre": "Rock", "duration": (8, 2), "file": "songs/Stairway to Heaven - Led Zeppelin (Remastered by NuDev).mp3"},
        {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock", "duration": (5, 55), "file": "songs/Queen - Bohemian Rhapsody - Remastered 2011.mp3"},
        {"title": "Hotel California", "artist": "Eagles", "genre": "Rock", "duration": (6, 30), "file": "songs/Hotel California - Eagles.mp3"},
        {"title": "Take Five", "artist": "Dave Brubeck", "genre": "Jazz", "duration": (5, 24), "file": "songs/Dave Brubeck - Take Five 1+.mp3"},
        {"title": "So What", "artist": "Miles Davis", "genre": "Jazz", "duration": (9, 22), "file": "songs/So What_.mp3"},
        {"title": "Billie Jean", "artist": "Michael Jackson", "genre": "Pop", "duration": (4, 54), "file": "songs/Billie Jean.mp3"},
        {"title": "Shape of You", "artist": "Ed Sheeran", "genre": "Pop", "duration": (3, 53), "file": "songs/Shape of You - Ed Sheeran.mp3"},
        {"title": "Strobe", "artist": "deadmau5", "genre": "Electronic", "duration": (10, 37), "file": None},
        {"title": "One More Time", "artist": "Daft Punk", "genre": "Electronic", "duration": (5, 20), "file": None},
        {"title": "Lose Yourself", "artist": "Eminem", "genre": "Hip Hop", "duration": (5, 26), "file": None},
        {"title": "N.Y. State of Mind", "artist": "Nas", "genre": "Hip Hop", "duration": (4, 53), "file": None},
        {"title": "Do I Wanna Know?", "artist": "Arctic Monkeys", "genre": "Indie", "duration": (4, 32), "file": None},
        {"title": "Master of Puppets", "artist": "Metallica", "genre": "Metal", "duration": (8, 35), "file": None},
        {"title": "Clair de Lune", "artist": "Claude Debussy", "genre": "Classical", "duration": (5, 5), "file": None},
        {"title": "Chill Study Beats", "artist": "Lofi Girl", "genre": "Lo-Fi", "duration": (2, 30), "file": None},
        {"title": "Midnight City", "artist": "M83", "genre": "Electronic", "duration": (4, 3), "file": None},
        {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "Rock", "duration": (5, 1), "file": "songs/Nirvana - Smells Like Teen Spirit slowed.mp3"},
        {"title": "Thriller", "artist": "Michael Jackson", "genre": "Pop", "duration": (5, 57), "file": "songs/08 - Michael Jackson - Thriller - Thriller.mp3"},
        {"title": "Blue in Green", "artist": "Miles Davis", "genre": "Jazz", "duration": (5, 37), "file": None},
        {"title": "Juicy", "artist": "The Notorious B.I.G.", "genre": "Hip Hop", "duration": (5, 2), "file": None},
    ]

    all_songs = []
    for data in songs_data:
        song, _ = Song.objects.get_or_create(
            title=data['title'], 
            artist=data['artist'], 
            defaults={
                'genre': genres[data['genre']], 
                'duration': timedelta(minutes=data['duration'][0], seconds=data['duration'][1]),
                'audio_file': data['file'] if data['file'] else ''
            }
        )
        all_songs.append(song)

    # 5. Mi Piace (Like alle canzoni da svariati utenti)
    print("-> Simulazione dei Like sulle canzoni...")
    for song in all_songs:
        # 0-5 likes casuali
        likers = random.sample(list(users.values()), k=random.randint(0, min(5, len(users))))
        song.likes.set(likers)

    # 6. Playlists (Editoriali, Pubbliche e Private)
    print("-> Creazione Playlist complesse...")
    
    # Editorial Playlists
    pl1, _ = Playlist.objects.get_or_create(name="Top 10 Global", owner=users['curator_demo'], defaults={'is_public': True, 'is_editorial': True})
    pl1.songs.set(random.sample(all_songs, 5))
    
    pl2, _ = Playlist.objects.get_or_create(name="Late Night Vibes", owner=users['curator_demo'], defaults={'is_public': True, 'is_editorial': True})
    pl2.songs.set(random.sample(all_songs, 6))

    # Public Playlists by Listeners
    pl3, _ = Playlist.objects.get_or_create(name="Alice's Favorites", owner=users['alice'], defaults={'is_public': True})
    pl3.songs.set(random.sample(all_songs, 4))

    pl4, _ = Playlist.objects.get_or_create(name="Bob's Rock Classics", owner=users['bob'], defaults={'is_public': True})
    pl4.songs.set([s for s in all_songs if s.genre.name == 'Rock'])

    # Private Playlist
    pl5, _ = Playlist.objects.get_or_create(name="Guilty Pleasures", owner=users['alice'], defaults={'is_public': False})
    pl5.songs.set(random.sample(all_songs, 3))
    
    # Playlist Followers
    pl1.followers.add(users['alice'], users['bob'], users['charlie'])
    pl3.followers.add(users['bob'], users['eve'])

    # 7. Commenti (Thread di discussione profondi e Like sui commenti)
    print("-> Creazione della canzone 'Perfetta' per la Demo...")
    song_target = next(s for s in all_songs if s.title == "Bohemian Rhapsody")
    
    # Record assoluto di Like: TUTTI gli utenti mettono Like a Bohemian Rhapsody
    song_target.likes.set(users.values())

    # Thread di discussione pazzesco
    c1, _ = Comment.objects.get_or_create(song=song_target, author=users['alice'], text="This is literally the best song ever written. 👑")
    c1.likes.add(users['bob'], users['charlie'], users['curator_demo'], users['admin_demo'])
    
    c2, _ = Comment.objects.get_or_create(song=song_target, author=users['bob'], text="Agreed! The vocal range is insane.", parent=c1)
    c2.likes.add(users['alice'])
    
    c_cur, _ = Comment.objects.get_or_create(song=song_target, author=users['curator_demo'], text="I just updated the high-quality audio file for this track. Let me know if you like it!")
    c_cur.likes.add(users['alice'], users['bob'], users['john_mod'])

    c_mod, _ = Comment.objects.get_or_create(song=song_target, author=users['moderator_demo'], text="Audio sounds perfect! I'm keeping an eye on these comments to keep the community safe 👀.", parent=c_cur)

    c_admin, _ = Comment.objects.get_or_create(song=song_target, author=users['admin_demo'], text="Welcome to the main hub of our project! Enjoy testing all the social features right here.")
    
    # SPAM Comment da far cancellare al Moderatore in fase di Demo
    Comment.objects.get_or_create(song=song_target, author=users['spambot'], text="FREE IPHONES!!! CLICK HERE -> http://spam-link.xyz/virus")

    song_target2 = next(s for s in all_songs if s.title == "Take Five")
    Comment.objects.get_or_create(song=song_target2, author=users['charlie'], text="That 5/4 time signature is so smooth.")

    # Altre canzoni minori

    # Thread su Lo-Fi
    song_target4 = next(s for s in all_songs if s.title == "Chill Study Beats")
    c_lofi1, _ = Comment.objects.get_or_create(song=song_target4, author=users['eve'], text="Listening to this while coding, perfectly relaxing.")
    c_lofi1.likes.add(users['alice'], users['frank'])
    Comment.objects.get_or_create(song=song_target4, author=users['alice'], text="Me too! It really helps to focus.", parent=c_lofi1)

    # Thread su Stairway to Heaven
    song_target5 = next(s for s in all_songs if s.title == "Stairway to Heaven")
    c_stair, _ = Comment.objects.get_or_create(song=song_target5, author=users['mike_curates'], text="The guitar solo at the end is legendary.")
    Comment.objects.get_or_create(song=song_target5, author=users['john_mod'], text="Absolutely. Page is a genius.", parent=c_stair)

    # Fine commenti

    print("✅ Popolamento del database completato con successo!")
    print("Ora puoi testare ruoli, amicizie, playlist private/pubbliche, audio player, e commenti annidati!")

if __name__ == '__main__':
    seed()
