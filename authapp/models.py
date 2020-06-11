""" authapp models
"""
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

# Create your models here.

class HoHooUser(AbstractUser):
    """ project User Model
    """
    userpic = models.ImageField(upload_to='userpic/', blank=True, verbose_name='аватар')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='отчество')
    occupation = models.CharField(max_length=60, blank=True, verbose_name='должность')
    phone = models.CharField(max_length=20, blank=True, verbose_name='номер телефона')
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    def delete(self, force_remove=False):
        self.is_active = False
        self.save()
        if force_remove:
            super().delete()

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


class Token(models.Model):
    user = models.OneToOneField(HoHooUser, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=40, verbose_name='код подтверждения')
    created = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created + timedelta(days=5) > now()


class UserProfile(models.Model):
    PAY_CASH = 'cash'
    PAY_CARD = 'card'
    PAY_CHECK = 'chck'

    PAYMENT_METHOD_CHOICES = (
        (PAY_CASH, 'Оплата наличными',),
        (PAY_CARD, 'Оплата банковской картой',),
        (PAY_CHECK, 'Безналичная оплата',),
    )

    user = models.OneToOneField(HoHooUser, on_delete=models.CASCADE, primary_key=True)
    payment = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES,
                        blank=True, verbose_name='предпочтительный метод оплаты')
    address = models.TextField(blank=True, verbose_name='адрес доставки')

    @receiver(post_save, sender=HoHooUser)
    def save_user_profile(sender, instance, created, *args, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        else:
            instance.userprofile.save()
