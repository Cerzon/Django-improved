""" basketapp context processors
"""
from .models import UserBasket


def user_basket(request):
    """ add user basket to context
    """
    basket = request.session.get('basket_id', None)
    if basket:
        try:
            basket = UserBasket.objects.get(pk=basket, state='active')
        except UserBasket.DoesNotExist:
            basket = UserBasket()
    else:
        basket = UserBasket()
    if request.user.is_authenticated:
        if not basket.slots.all():
            try:
                basket = UserBasket.objects.get(
                    customer=request.user, state='active')
            except UserBasket.MultipleObjectsReturned:
                basket = UserBasket.objects.filter(
                    customer=request.user, state='active').first()
                UserBasket.objects.filter(
                    customer=request.user, state='active'
                    ).exclude(pk=basket.pk).update(state='delete')
            except UserBasket.DoesNotExist:
                basket = UserBasket()
        if basket.customer and basket.customer != request.user:
            basket = UserBasket()
        basket.customer = request.user
    elif basket.customer:
        basket = UserBasket()
    basket.save()
    request.session['basket_id'] = basket.pk
    return {'basket': basket}
