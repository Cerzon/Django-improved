""" basketapp views
"""
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from mainapp.models import Product
from .models import UserBasket, BasketSlot

# Create your views here.

def get_basket(request):
    """ получение корзины, проверка и привязка её к пользователю
        если пользователь залогинен
    """
    basket = request.session.get('basket_id', None)
    # если id корзины сохранён в сессии
    if basket:
        try:
            basket = UserBasket.objects.get(pk=basket, state='active')
        except UserBasket.DoesNotExist:
            basket = UserBasket()
    else:
        basket = UserBasket()
    # так или иначе, к этому моменту объект корзины уже существует
    if request.user.is_authenticated:
        # если юзер залогинен
        if not basket.slots.all():
            # если уже найденная корзина пуста, но юзер залогинен, у него
            # может быть прежняя незакрытая корзина
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
            # если подцепилась чужая хозная корзина, создаём юзеру новую
            basket = UserBasket()
        basket.customer = request.user
    elif basket.customer:
        # если юзер не залогинен, а корзина хозная, создаём новую бесхозную
        basket = UserBasket()
    basket.save()
    request.session['basket_id'] = basket.pk
    return basket


def index(request):
    """ basket base view
        list of slots
    """
    context = {
        'page_title': 'Корзина',
        'content_header': 'Корзина',
    }
    basket = get_basket(request)
    context['slots'] = basket.slots.all().select_related()
    return render(request, 'basketapp/index.html', context)


def add_product(request, product_id):
    """ add basket slot or increase slot quantity
    """
    product = get_object_or_404(Product, pk=product_id)
    basket = get_basket(request)
    slot, created = basket.slots.get_or_create(product=product)
    if not created:
        slot.quantity = F('quantity') + 1
    slot.save()
    if request.is_ajax():
        return JsonResponse(basket.total)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_product(request, product_id):
    """ decrease basket slot quantity
    """
    if request.session.get('basket_id', False):
        product = get_object_or_404(Product, pk=product_id)
        basket = get_basket(request)
        try:
            slot = basket.slots.get(product=product)
        except BasketSlot.DoesNotExist:
            slot = None
        if slot:
            if slot.quantity == 1:
                slot.delete()
            else:
                slot.quantity = F('quantity') - 1
                slot.save()
        if request.is_ajax():
            return JsonResponse(basket.total)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_slot(request, slot_id):
    """ remove slot from basket
    """
    if request.session.get('basket_id', False):
        basket = get_basket(request)
        try:
            slot = basket.slots.get(pk=slot_id)
        except BasketSlot.DoesNotExist:
            slot = None
        else:
            slot.delete()
        if request.is_ajax():
            return JsonResponse(basket.total)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
