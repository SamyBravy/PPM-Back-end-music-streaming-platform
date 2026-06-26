from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Vista di registrazione — usa il form personalizzato con campo role."""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, FriendRequest
from .forms import UserProfileUpdateForm

class UserProfileView(LoginRequiredMixin, TemplateView):
    """Pagina del profilo utente privato (personale)."""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['pending_requests'] = user.received_requests.filter(is_accepted=False)
        context['friends_list'] = user.friends.all()
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Vista per modificare il proprio profilo."""
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PublicProfileView(LoginRequiredMixin, DetailView):
    """Profilo pubblico di un altro utente."""
    model = CustomUser
    template_name = 'users/public_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'target_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.object
        current_user = self.request.user
        
        context['user_comments'] = target_user.comments.all()
        
        # Gestione stato amicizia
        is_friend = current_user.friends.filter(pk=target_user.pk).exists()
        is_self = current_user == target_user
        
        context['is_friend'] = is_friend
        
        if is_self:
            from django.db.models import Q
            context['public_playlists'] = target_user.playlists.filter(Q(is_public=True) | Q(is_editorial=True)).distinct()
        elif is_friend:
            context['public_playlists'] = target_user.playlists.filter(is_public=True)
        else:
            context['public_playlists'] = target_user.playlists.filter(is_editorial=True)
            
        if not is_friend and not is_self:
            # Check if a friend request is pending
            req_sent = FriendRequest.objects.filter(sender=current_user, receiver=target_user, is_accepted=False).exists()
            req_received = FriendRequest.objects.filter(sender=target_user, receiver=current_user, is_accepted=False).exists()
            context['request_sent'] = req_sent
            context['request_received'] = req_received

        return context


@login_required
def send_friend_request_by_username(request):
    from django.contrib import messages
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        if not username:
            messages.error(request, "Please enter a valid username.")
            return redirect('users:profile')
            
        try:
            target_user = CustomUser.objects.get(username=username)
            if target_user == request.user:
                messages.warning(request, "You cannot send a friend request to yourself.")
            elif request.user.friends.filter(pk=target_user.pk).exists():
                messages.info(request, f"You are already friends with {username}.")
            else:
                FriendRequest.objects.get_or_create(sender=request.user, receiver=target_user)
                messages.success(request, f"Friend request sent to {username}.")
        except CustomUser.DoesNotExist:
            messages.error(request, f"The user '{username}' does not exist.")
            
    return redirect('users:profile')


@login_required
def send_friend_request(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    if target_user != request.user:
        FriendRequest.objects.get_or_create(sender=request.user, receiver=target_user)
    return redirect('users:public_profile', username=username)


@login_required
def accept_friend_request(request, request_id):
    friend_req = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_req.is_accepted = True
    friend_req.save()
    request.user.friends.add(friend_req.sender)
    friend_req.sender.friends.add(request.user)
    return redirect('users:profile')


@login_required
def reject_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
        friend_request.delete()
    return redirect('users:profile')

@login_required
def remove_friend(request, username):
    from django.contrib import messages
    target_user = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        if request.user.friends.filter(pk=target_user.pk).exists():
            request.user.friends.remove(target_user)
            # Remove previous requests in both directions
            FriendRequest.objects.filter(sender=request.user, receiver=target_user).delete()
            FriendRequest.objects.filter(sender=target_user, receiver=request.user).delete()
            messages.success(request, f"You have removed {username} from your friends.")
    return redirect('users:public_profile', username=username)
