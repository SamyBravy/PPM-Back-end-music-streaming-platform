from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.db.models import Q
from .models import Song, Playlist, Genre

class SongListView(LoginRequiredMixin, ListView):
    """Vista catalogo brani — protetta da login."""
    model = Song
    template_name = 'music/song_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        genre_id = self.request.GET.get('genre', '')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(artist__icontains=q)
            )
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['current_q'] = self.request.GET.get('q', '')
        context['current_genre'] = self.request.GET.get('genre', '')
        return context


class SongCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Creazione brano — solo Curator (permission: music.add_song)."""
    model = Song
    template_name = 'music/song_form.html'
    fields = ['title', 'artist', 'genre', 'duration']
    permission_required = 'music.add_song'


class SongUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Modifica brano — solo Curator (permission: music.change_song)."""
    model = Song
    template_name = 'music/song_form.html'
    fields = ['title', 'artist', 'genre', 'duration']
    permission_required = 'music.change_song'


class SongDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Eliminazione brano — solo Curator (permission: music.delete_song)."""
    model = Song
    template_name = 'music/song_confirm_delete.html'
    success_url = reverse_lazy('music:song_list')
    permission_required = 'music.delete_song'


from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Song, Playlist, Genre, Comment
from .forms import CommentForm

class SongDetailView(LoginRequiredMixin, DetailView):
    """Vista dettaglio brano con commenti."""
    model = Song
    template_name = 'music/song_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        if self.request.user.is_authenticated:
            context['user_playlists'] = Playlist.objects.filter(owner=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.song = self.object
            comment.author = request.user
            comment.save()
            return redirect('music:song_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminazione commento — solo staff (moderatori)."""
    model = Comment
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('music:song_detail', kwargs={'pk': self.object.song.pk})

class PlaylistListView(LoginRequiredMixin, ListView):
    """Vista lista playlist — protetta da login."""
    model = Playlist
    template_name = 'music/playlist_list.html'

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)

class PlaylistDetailView(LoginRequiredMixin, DetailView):
    """Vista dettaglio playlist — mostra le canzoni all'interno."""
    model = Playlist
    template_name = 'music/playlist_detail.html'

    def get_queryset(self):
        from django.db.models import Q
        return Playlist.objects.filter(Q(owner=self.request.user) | Q(is_public=True))


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    """Creazione playlist — per qualsiasi utente autenticato."""
    model = Playlist
    template_name = 'music/playlist_form.html'
    fields = ['name', 'is_public']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        song_id = self.request.GET.get('add_song_id')
        if song_id:
            from .models import Song
            from django.shortcuts import get_object_or_404
            from django.contrib import messages
            song = get_object_or_404(Song, id=song_id)
            self.object.songs.add(song)
            messages.success(self.request, f"Playlist creata e '{song.title}' aggiunta con successo!")
        return response


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    """Modifica di una playlist (es. cambiarne il nome o renderla pubblica/privata)."""
    model = Playlist
    template_name = 'music/playlist_form.html'
    fields = ['name', 'is_public']

    def get_queryset(self):
        # L'utente può modificare solo le TUE playlist
        return Playlist.objects.filter(owner=self.request.user)


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def add_song_to_playlist(request, song_id, playlist_id):
    """Aggiunge un brano a una playlist specifica, previa verifica della ownership."""
    from django.contrib import messages
    song = get_object_or_404(Song, id=song_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    
    if song in playlist.songs.all():
        messages.info(request, f"'{song.title}' è già presente in {playlist.name}.")
    else:
        playlist.songs.add(song)
        messages.success(request, f"'{song.title}' aggiunta a {playlist.name}!")
        
    return redirect(request.META.get('HTTP_REFERER', 'music:song_list'))


@login_required
def remove_song_from_playlist(request, song_id, playlist_id):
    """Rimuove un brano da una playlist specifica, previa verifica della ownership."""
    song = get_object_or_404(Song, id=song_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    playlist.songs.remove(song)
    return redirect('music:playlist_detail', pk=playlist.id)


class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminazione playlist — solo per il proprietario."""
    model = Playlist
    template_name = 'music/playlist_confirm_delete.html'
    success_url = reverse_lazy('music:playlist_list')

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)
