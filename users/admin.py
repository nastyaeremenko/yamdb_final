from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    CustomUserAdmin class represent to Admin for custom user
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'email',
        'is_staff',
        'is_active',
        'role',
    )
    list_filter = (
        'email',
        'is_staff',
        'is_active',
        'role',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_active',
                    'role',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                    'role',
                ),
            },
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
