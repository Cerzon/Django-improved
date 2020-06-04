""" basketapp URL Configuration
"""
from django.urls import path
from basketapp import views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.index, name='index'),
    path('add/<int:product_id>/', basketapp.add_product, name='add_product'),
    path('remove/<int:product_id>/', basketapp.remove_product, name='remove_product'),
    path('delete/<int:slot_id>/', basketapp.delete_slot, name='delete_slot'),
]
