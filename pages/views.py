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
            # 1. Trova il genere più presente nelle playlist dell'utente
            top_genre = Genre.objects.filter(
                songs__playlists__owner=user
            ).annotate(
                song_count=Count('songs')
            ).order_by('-song_count').first()
            
            if top_genre:
                # 2. Suggerisci le ultime novità di quel genere, escludendo brani che ha già
                recommended_list = list(Song.objects.filter(genre=top_genre).exclude(
                    playlists__owner=user
                ).order_by('-created_at')[:3])
                
                # Se non abbiamo 3 brani di quel genere, riempiamo con altri brani recenti
                if len(recommended_list) < 3:
                    needed = 3 - len(recommended_list)
                    already_ids = [s.id for s in recommended_list]
                    fallback_songs = Song.objects.exclude(playlists__owner=user).exclude(id__in=already_ids).order_by('-created_at')[:needed]
                    recommended_list.extend(fallback_songs)
                
                recommended = recommended_list

        # 3. Fallback sensato se l'utente è nuovo (nessuna playlist) o non è loggato:
        # Mostriamo gli ultimi 3 brani aggiunti in assoluto al catalogo
        if not recommended or len(recommended) == 0:
            if user.is_authenticated:
                recommended = Song.objects.exclude(playlists__owner=user).order_by('-created_at')[:3]
            else:
                recommended = Song.objects.order_by('-created_at')[:3]
            
        context['recommended_songs'] = recommended
        if user.is_authenticated:
            context['user_playlists'] = Playlist.objects.filter(owner=user)
        return context
