from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    SignUpView, 
    UserProfileView, 
    ProfileUpdateView, 
    PublicProfileView,
    send_friend_request,
    remove_friend,
    send_friend_request_by_username,
    accept_friend_request,
    reject_friend_request
)

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    
    path('profile/<str:username>/', PublicProfileView.as_view(), name='public_profile'),
    path('profile/<str:username>/add/', send_friend_request, name='send_request'),
    path('profile/<str:username>/remove/', remove_friend, name='remove_friend'),
    path('profile/add_friend_by_username/submit/', send_friend_request_by_username, name='send_request_by_username'),
    path('requests/<int:request_id>/accept/', accept_friend_request, name='accept_request'),
    path('requests/<int:request_id>/reject/', reject_friend_request, name='reject_request'),
]
