from django import forms
from .models import Comment, Playlist

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
        if user and not user.is_staff:
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

