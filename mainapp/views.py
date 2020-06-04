""" mainapp views
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authapp.models import HoHooUser
from .models import Category, Product
# from django.views.generic import ListView, DetailView

# Create your views here.

# class IndexView(ListView):
#     template_name = 'mainapp/index.html'

def index(request):
    """ main page view
    """
    context = {
        'page_title': 'Главная',
        'content_header': 'Команда профессионалов',
    }
    staff = HoHooUser.objects.filter(public=True)
    if staff:
        context['object_list'] = staff
    return render(request, 'mainapp/index.html', context)


def products(request, category=None, page=None):
    """ product catalog view
    """
    context = {
        'page_title': 'Каталог',
        'content_header': 'Каталог товаров',
    }
    context['category_list'] = Category.objects.filter(is_active=True)
    goods = Product.objects.all().select_related()
    if category:
        goods = goods.filter(category__slug=category)
    if goods:
        if len(goods) > 4:
            paginator = Paginator(goods, 4)
            try:
                page_goods = paginator.page(page)
            except PageNotAnInteger:
                page_goods = paginator.page(1)
            except EmptyPage:
                page_goods = paginator.page(paginator.num_pages)
            context.update({
                'object_list': page_goods,
                'paginated': True,
                'page_prev_url': None,
                'page_next_url': None,
            })
            if category:
                if page_goods.has_previous():
                    context['page_prev_url'] = reverse(
                        'mainapp:catalog:category_page',
                        kwargs={'category': category, 'page': page_goods.previous_page_number()})
                if page_goods.has_next():
                    context['page_next_url'] = reverse(
                        'mainapp:catalog:category_page',
                        kwargs={'category': category, 'page': page_goods.next_page_number()})
            else:
                if page_goods.has_previous():
                    context['page_prev_url'] = reverse(
                        'mainapp:catalog:index_page',
                        kwargs={'page': page_goods.previous_page_number()})
                if page_goods.has_next():
                    context['page_next_url'] = reverse(
                        'mainapp:catalog:index_page',
                        kwargs={'page': page_goods.next_page_number()})
        else:
            context['object_list'] = goods
        context['popular'] = goods.annotate(
            num=Count('slots')).order_by('num')[:4]
    return render(request, 'mainapp/products.html', context)


def product_detail(request, category, product):
    """ product details view
    """
    try:
        obj = Product.objects.get(slug=product, category__slug=category)
    except Product.DoesNotExist:
        return HttpResponseRedirect(reverse('mainapp:catalog:index'))
    context = {
        'content_header': 'Страница товара'
    }
    context['page_title'] = 'Товар - {}'.format(obj.name)
    context['object'] = obj
    context['recomend'] = Product.objects.filter(
        category=obj.category).exclude(pk=obj.pk).order_by('?')[:4]
    return render(request, 'mainapp/product_detail.html', context)


def contacts(request):
    """ contacts page view
    """
    context = {
        'page_title': 'Контакты',
        'content_header': 'Наши контакты',
    }
    return render(request, 'mainapp/contacts.html', context)
