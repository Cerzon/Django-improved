""" mainapp URL Configuration
"""
from django.urls import path, include
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('contacts/', mainapp.contacts, name='contacts'),
    path('products/', include(([
        path('', mainapp.products, name='index'),
        path('page/<int:page>/', mainapp.products, name='index_page'),
        path('<slug:category>/', mainapp.products, name='category'),
        path('<slug:category>/page/<int:page>/', mainapp.products, name='category_page'),
        path('<slug:category>/<slug:product>/', mainapp.product_detail, name='product'),
    ], 'catalog'))),
]
