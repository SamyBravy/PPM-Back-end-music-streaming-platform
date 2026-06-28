from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Implements a role system (Listener, Curator, Moderator), 
    friend management, and custom profile icons.
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
    """Model to handle friend requests between users."""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"Da {self.sender.username} a {self.receiver.username} (Accettata: {self.is_accepted})"
