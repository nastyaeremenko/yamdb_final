from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form to represent creation User with role
    """
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'username', 'role')


class CustomUserChangeForm(UserChangeForm):
    """
    Form to represent changing User with role
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'role')
