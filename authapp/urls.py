""" authapp URL Configuration
"""
from django.urls import path, re_path
from authapp import views as authapp

app_name = 'authapp'

urlpatterns = [
    path('', authapp.index, name='index'),
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('signup/', authapp.UserRegisterView.as_view(), name='signup'),
    path('logout/', authapp.user_logout, name='logout'),
    path('edit/', authapp.UserProfileEditView.as_view(), name='edit'),
    re_path(r'^verify/user_(?P<username>[@\w][@\w\.\-\+]+)/$',
            authapp.user_verify, name='verify_form'),
    re_path(r'^verify/(?P<code>\w+)/$', authapp.user_verify, name='verify'),
]
