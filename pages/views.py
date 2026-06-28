from django.views.generic import TemplateView
from django.db.models import Count
from music.models import Song, Genre, Playlist

class HomePageView(TemplateView):
    """Vista della homepage — con logica di raccomandazione brani."""
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recommended = None
        user = self.request.user
        
        if user.is_authenticated:
            from django.db.models import Q
            
            # Trova i brani che piacciono all'utente
            liked_or_playlist_songs = Song.objects.filter(
                Q(playlists__owner=user) | Q(likes=user)
            ).distinct()
            
            # 1. Trova il genere più presente
            top_genre_data = liked_or_playlist_songs.values('genre').annotate(
                count=Count('id')
            ).order_by('-count').first()
            top_genre_id = top_genre_data['genre'] if top_genre_data else None

            # 2. Trova l'artista più presente
            top_artist_data = liked_or_playlist_songs.values('artist').annotate(
                count=Count('id')
            ).order_by('-count').first()
            top_artist = top_artist_data['artist'] if top_artist_data else None
            
            # Base query: exclude songs in playlists and liked songs
            base_qs = Song.objects.annotate(likes_count=Count('likes')).exclude(
                playlists__owner=user
            ).exclude(
                likes=user
            )
            
            if top_genre_id or top_artist:
                # 3. Suggerisci novità dello stesso genere o stesso artista
                q_filters = Q()
                if top_genre_id:
                    q_filters |= Q(genre_id=top_genre_id)
                if top_artist:
                    q_filters |= Q(artist=top_artist)
                    
                recommended_list = list(base_qs.filter(q_filters).order_by('?')[:3])
                
                # Se non abbiamo 3 brani, riempiamo con altri
                if len(recommended_list) < 3:
                    needed = 3 - len(recommended_list)
                    already_ids = [s.id for s in recommended_list]
                    fallback_songs = base_qs.exclude(id__in=already_ids).order_by('?')[:needed]
                    recommended_list.extend(fallback_songs)
                
                recommended = recommended_list

        # 3. Fallback se l'utente non è loggato o non ha raccomandazioni
        if not recommended or len(recommended) == 0:
            if user.is_authenticated:
                recommended = Song.objects.annotate(likes_count=Count('likes')).exclude(
                    playlists__owner=user
                ).exclude(likes=user).order_by('?')[:3]
            else:
                recommended = Song.objects.annotate(likes_count=Count('likes')).order_by('-created_at')[:3]
        
        context['recommended_songs'] = recommended
        context['latest_additions'] = Song.objects.annotate(likes_count=Count('likes')).order_by('-created_at')[:3]
        context['trending_songs'] = Song.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:4]
        if user.is_authenticated:
            context['user_playlists'] = Playlist.objects.filter(owner=user)
        return context
