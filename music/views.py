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
        
        current_genre_id = self.request.GET.get('genre', '')
        context['current_q'] = self.request.GET.get('q', '')
        context['current_genre'] = current_genre_id
        
        if current_genre_id:
            try:
                context['current_genre_obj'] = Genre.objects.get(id=current_genre_id)
            except Genre.DoesNotExist:
                pass
                
        return context


class SongCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Creazione brano — solo Curator (permission: music.add_song)."""
    model = Song
    template_name = 'music/song_form.html'
    fields = ['title', 'artist', 'genre', 'duration', 'audio_file']
    permission_required = 'music.add_song'


class SongUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Modifica brano — solo Curator (permission: music.change_song)."""
    model = Song
    template_name = 'music/song_form.html'
    fields = ['title', 'artist', 'genre', 'duration', 'audio_file']
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
from .forms import CommentForm, PlaylistForm

class SongDetailView(LoginRequiredMixin, DetailView):
    """Vista dettaglio brano con commenti."""
    model = Song
    template_name = 'music/song_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['top_level_comments'] = self.object.comments.filter(parent__isnull=True)
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
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    comment.parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    pass
            comment.save()
            return redirect('music:song_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminazione commento — solo staff (moderatori)."""
    model = Comment
    
    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if not request.user.is_staff and not request.user.is_superuser and request.user != comment.author:
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['famous_playlists'] = Playlist.objects.filter(is_editorial=True).exclude(owner=self.request.user)
        context['favorite_playlists'] = self.request.user.favorite_playlists.all()
        context['liked_songs'] = self.request.user.liked_songs.all()
        return context

class PlaylistDetailView(LoginRequiredMixin, DetailView):
    """Vista dettaglio playlist — mostra le canzoni all'interno."""
    model = Playlist
    template_name = 'music/playlist_detail.html'

    def get_queryset(self):
        from django.db.models import Q
        return Playlist.objects.filter(
            Q(owner=self.request.user) | 
            Q(is_editorial=True) | 
            (Q(is_public=True) & Q(owner__friends=self.request.user))
        ).distinct()


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    """Creazione playlist — per qualsiasi utente autenticato."""
    model = Playlist
    template_name = 'music/playlist_form.html'
    form_class = PlaylistForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
            messages.success(self.request, f"Playlist created and '{song.title}' added successfully!")
        return response


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    """Modifica di una playlist (es. cambiarne il nome o renderla pubblica/privata)."""
    model = Playlist
    template_name = 'music/playlist_form.html'
    form_class = PlaylistForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            from django.db.models import Q
            return Playlist.objects.filter(Q(owner=self.request.user) | Q(is_editorial=True))
        # L'utente normale può modificare solo le SUE playlist
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
        messages.info(request, f"'{song.title}' is already in {playlist.name}.")
    else:
        playlist.songs.add(song)
        messages.success(request, f"'{song.title}' added to {playlist.name}!")
        
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
        if self.request.user.is_staff or self.request.user.is_superuser:
            from django.db.models import Q
            return Playlist.objects.filter(Q(owner=self.request.user) | Q(is_editorial=True))
        return Playlist.objects.filter(owner=self.request.user)

@login_required
def toggle_favorite_playlist(request, pk):
    """Aggiunge o rimuove una playlist dai preferiti."""
    playlist = get_object_or_404(Playlist, pk=pk)
    if request.user in playlist.followers.all():
        playlist.followers.remove(request.user)
    else:
        playlist.followers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'music:playlist_list'))

from django.contrib.auth.mixins import UserPassesTestMixin

class CuratorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class GenreListView(LoginRequiredMixin, CuratorRequiredMixin, ListView):
    """Lista dei generi — solo Curator."""
    model = Genre
    template_name = 'music/genre_list.html'

class GenreCreateView(LoginRequiredMixin, CuratorRequiredMixin, CreateView):
    """Creazione genere — solo Curator."""
    model = Genre
    template_name = 'music/genre_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('music:genre_list')

class GenreUpdateView(LoginRequiredMixin, CuratorRequiredMixin, UpdateView):
    """Modifica genere — solo Curator."""
    model = Genre
    template_name = 'music/genre_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('music:genre_list')

class GenreDeleteView(LoginRequiredMixin, CuratorRequiredMixin, DeleteView):
    """Eliminazione genere — solo Curator."""
    model = Genre
    template_name = 'music/genre_confirm_delete.html'
    success_url = reverse_lazy('music:genre_list')

@login_required
def toggle_like_song(request, pk):
    """Aggiunge o rimuove una canzone dai preferiti (Liked Songs)."""
    song = get_object_or_404(Song, pk=pk)
    if request.user in song.likes.all():
        song.likes.remove(request.user)
    else:
        song.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'music:song_list'))
