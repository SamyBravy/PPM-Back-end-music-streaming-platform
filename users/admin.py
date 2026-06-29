from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, FriendRequest


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom User Info', {'fields': ('role', 'birth_date', 'profile_icon', 'friends')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom User Info', {'fields': ('role', 'birth_date', 'profile_icon')}),
    )

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'is_accepted', 'created_at']
    list_filter = ['is_accepted', 'created_at']
    search_fields = ['sender__username', 'receiver__username']

admin.site.register(CustomUser, CustomUserAdmin)
