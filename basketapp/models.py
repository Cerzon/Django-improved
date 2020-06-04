""" basketapp models
"""
from django.db import models
from django.db.models import Count, F, Sum
from django.utils.functional import cached_property
from authapp.models import HoHooUser
from mainapp.models import Product

# Create your models here.

class UserBasket(models.Model):
    """ корзина юзера. может работать с анонимусом
    """
    STATE_CHOICES = (
        ('active', 'активная корзина',),
        ('chkout', 'оформлен заказ',),
        ('archiv', 'история заказов',),
        ('delete', 'корзина удалена',),
    )
    started = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    customer = models.ForeignKey(
        HoHooUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='baskets',
        verbose_name='покупатель'
    )
    state = models.CharField(
        max_length=6,
        choices=STATE_CHOICES,
        default='active',
        verbose_name='статус'
    )

    class Meta:
        ordering = ('-started',)
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        username = 'anonymous'
        if self.customer:
            username = self.customer.username
        return 'Корзина пользователя {} от {}'.format(
            username, self.started.strftime('%d %b %Y')
        )

    @cached_property
    def total(self):
        """ возвращает словарь с суммарными данными о корзине
        """
        res = self.slots.aggregate(
            cost=Sum(
                F('product__price') * F('quantity'),
                output_field=models.DecimalField()),
            slots=Count('pk'),
            items=Sum('quantity')
        )
        return {key: value or 0 for key, value in res.items()}


class BasketSlot(models.Model):
    """ товарные позиции корзины
    """
    basket = models.ForeignKey(
        UserBasket,
        on_delete=models.CASCADE,
        related_name='slots',
        verbose_name='заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='slots',
        verbose_name='товар'
    )
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='количество')

    class Meta:
        ordering = ('basket',)
        verbose_name = 'товар корзины'
        verbose_name_plural = 'товары корзины'

    def __str__(self):
        username = 'anonymous'
        if self.basket.customer:
            username = self.basket.customer.username
        return '({}) {} - {}'.format(username, self.product.name, self.quantity)

    @property
    def cost(self):
        """ возвращает стоимость слота
        """
        return self.product.price * self.quantity
