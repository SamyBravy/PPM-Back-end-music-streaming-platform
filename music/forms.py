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
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('editorial', 'Editorial'),
    )

    visibility = forms.ChoiceField(
        choices=VISIBILITY_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = Playlist
        fields = ['name']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.user = user

        if user and (user.role == 'curator' or user.is_superuser):
            self.fields['visibility'].choices = self.VISIBILITY_CHOICES
        else:
            self.fields['visibility'].choices = self.VISIBILITY_CHOICES[:2]

        if self.instance and self.instance.pk:
            if self.instance.is_editorial:
                self.fields['visibility'].initial = 'editorial'
            elif self.instance.is_public:
                self.fields['visibility'].initial = 'public'
            else:
                self.fields['visibility'].initial = 'private'
        else:
            self.fields['visibility'].initial = 'private'

    def clean(self):
        cleaned_data = super().clean()
        visibility = cleaned_data.get('visibility')
        if visibility == 'editorial':
            if not self.user or (self.user.role != 'curator' and not self.user.is_superuser):
                raise forms.ValidationError("You are not allowed to create editorial playlists.")
            cleaned_data['is_public'] = True
            cleaned_data['is_editorial'] = True
        elif visibility == 'public':
            cleaned_data['is_public'] = True
            cleaned_data['is_editorial'] = False
        else:
            cleaned_data['is_public'] = False
            cleaned_data['is_editorial'] = False
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        visibility = self.cleaned_data.get('visibility')

        instance.is_editorial = visibility == 'editorial'
        instance.is_public = visibility in ('public', 'editorial')

        if commit:
            instance.save()
            self.save_m2m()
        return instance

