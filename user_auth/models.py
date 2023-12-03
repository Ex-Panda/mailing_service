import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

NULLABLE = {'blank': True, 'null': True}


def generation_password():
    list_password = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    list_code = random.sample(list_password, 10)
    result = ''.join(list_code)
    return result


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    avatar = models.ImageField(verbose_name='аватар', **NULLABLE)
    phone_number = models.IntegerField(_("phone number"), **NULLABLE)
    country = models.CharField(_("country"), max_length=50, **NULLABLE)

    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    verification_code = models.CharField(max_length=50, verbose_name='проверочный код', default=generation_password)

