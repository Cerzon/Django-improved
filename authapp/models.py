""" authapp models
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class HoHooUser(AbstractUser):
    """ project User Model
    """
    userpic = models.ImageField(upload_to='userpic/', blank=True, verbose_name='аватар')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='отчество')
    occupation = models.CharField(max_length=60, blank=True, verbose_name='должность')
    phone = models.CharField(max_length=20, blank=True, verbose_name='номер телефона')
    public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name='аккаунт активен')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    def delete(self):
        self.is_active = False
        self.save()

    @property
    def full_name(self):
        result = '{} {} {}'.format(self.last_name, self.first_name, self.middle_name)
        return result.strip()

    @property
    def short_name(self):
        result = '{} {}'.format(self.first_name, self.last_name)
        return result.strip()

    def quote(self):
        result = self.quotes.filter(product__isnull=True).order_by('?')
        if result:
            result = result[0]
        return result
