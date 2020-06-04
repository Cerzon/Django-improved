""" authapp URL Configuration
"""
from django.urls import path, include
from adminapp import views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('users/', include(([
        path('', adminapp.UserListView.as_view(), name='list'),
        path('create/', adminapp.CreateUserView.as_view(), name='create'),
        path('update/<int:pk>/', adminapp.UpdateUserView.as_view(), name='update'),
        path('delete/<int:pk>/', adminapp.DeleteUserView.as_view(), name='delete'),
    ], 'user'))),
    path('categories/', include(([
        path('', adminapp.CategoryListView.as_view(), name='list'),
        path('create/', adminapp.CreateCategoryView.as_view(), name='create'),
        path('update/<int:pk>/', adminapp.UpdateCategoryView.as_view(), name='update'),
        path('delete/<int:pk>/', adminapp.DeleteCategoryView.as_view(), name='delete'),
    ], 'category'))),
    path('products/', include(([
        path('', adminapp.ProductListView.as_view(), name='list'),
        path('category/<int:pk>/', adminapp.ProductListView.as_view(), name='filter_list'),
        path('create/', adminapp.CreateProductView.as_view(), name='create'),
        path('update/<int:pk>/', adminapp.UpdateProductView.as_view(), name='update'),
        path('delete/<int:pk>/', adminapp.DeleteProductView.as_view(), name='delete'),
    ], 'product'))),
]
