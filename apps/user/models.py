from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.user.enum import UserRoleEnum
from apps.user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователи"""

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, null=True)
    full_name = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=UserRoleEnum.choices, default=UserRoleEnum.BUYER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    blocked_at = models.DateTimeField(null=True)
    password = models.CharField(_("password"), max_length=128, blank=True, null=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ["id"]

