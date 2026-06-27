from django import forms
from .models import Comment, Playlist, Song

class CustomAudioFileInput(forms.ClearableFileInput):
    template_name = 'music/widgets/custom_audio_file.html'

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'duration', 'audio_file']
        widgets = {
            'audio_file': CustomAudioFileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Check if the user checked the clear checkbox in the bound data
        is_cleared = self.is_bound and self.data.get(self.add_prefix('audio_file') + '-clear')
        
        if self.instance and self.instance.pk and self.instance.audio_file and not is_cleared:
            self.fields['duration'].widget.attrs['readonly'] = True
            self.fields['duration'].widget.attrs['style'] = 'background-color: #e9ecef; pointer-events: none;'
            
        if is_cleared:
            self.fields['audio_file'].widget.attrs['data_cleared'] = 'true'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Write a comment...'
            })
        }
        labels = {
            'text': ''
        }

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'is_public', 'is_editorial']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role != 'curator' and not user.is_superuser:
            self.fields.pop('is_editorial')
        else:
            self.fields['is_editorial'].label = "🌟 Editorial"
        
        self.fields['is_public'].label = "👥 Public"

    def clean(self):
        cleaned_data = super().clean()
        is_editorial = cleaned_data.get('is_editorial')
        if is_editorial:
            cleaned_data['is_public'] = True
        return cleaned_data

