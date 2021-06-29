from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class CustomUser(AbstractUser):
    """
    A class to represent a USER.

    some attributes
    ----------
    username = models.CharField
        username.
    email = models.EmailField
        email.
    first_name = models.CharField
        first name.
    last_name = models.CharField
        last name.
    role = models.CharField
        role(privileges).
    bio = models.TextField
        About user.
    """
    class UserRole(models.TextChoices):
        USER = 'user', _('user')
        MODERATOR = ('moderator', _('moderator'))
        ADMIN = 'admin', _('admin')

    username = models.CharField(
        db_index=True, max_length=255, unique=True, null=True
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        verbose_name='email',
    )
    first_name = models.CharField(
        max_length=255, null=True, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=255, null=True, verbose_name='Фамилия'
    )
    role = models.CharField(
        max_length=255,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Пользовательская роль',
    )
    bio = models.TextField(max_length=1000, null=True, verbose_name='О себе')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR
