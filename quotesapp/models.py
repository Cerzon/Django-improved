""" quotesapp model
"""
from django.db import models
from authapp.models import HoHooUser
from mainapp.models import Product

# Create your models here.

class UserQuote(models.Model):
    """ model contains user quotes and feedback for products
    """
    author = models.ForeignKey(HoHooUser, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField(verbose_name='текст')
    header = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        null=True, related_name='feedback'
    )

    class Meta:
        ordering = ('author',)
        verbose_name = 'цитата'
        verbose_name_plural = 'цитаты'

    def __str__(self):
        return '{}: {:40.40}'.format(self.author.short_name, self.text)
