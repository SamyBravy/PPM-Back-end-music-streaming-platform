from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
    """
    Modello utente personalizzato.
    Estende AbstractUser per consentire future estensioni
    (es. avatar, bio, ruolo listener/curator).
    Il ruolo Curator è gestito anche tramite il campo is_staff ereditato da AbstractUser.
    """
    ROLE_CHOICES = (
        ('listener', 'Listener'),
        ('curator', 'Curator'),
        ('moderator', 'Moderator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='listener')
    birth_date = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField('self', blank=True)

    ICON_CHOICES = [
        ('👤', '👤'),
        ('🐶', '🐶'),
        ('🐱', '🐱'),
        ('🦊', '🦊'),
        ('🐯', '🐯'),
        ('🐼', '🐼'),
        ('🐰', '🐰'),
        ('👽', '👽'),
        ('🤖', '🤖'),
        ('👻', '👻'),
        ('🤠', '🤠'),
    ]
    profile_icon = models.CharField(max_length=10, choices=ICON_CHOICES, default='👤')

    @property
    def pending_friend_requests_count(self):
        return self.received_requests.filter(is_accepted=False).count()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class FriendRequest(models.Model):
    """Modello per gestire le richieste di amicizia tra utenti."""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"Da {self.sender.username} a {self.receiver.username} (Accettata: {self.is_accepted})"
