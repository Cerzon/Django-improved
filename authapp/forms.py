""" forms for register, update and login user
"""
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.core import validators
from .models import HoHooUser


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = HoHooUser
        fields = (
            'username',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    phone = forms.CharField(label='Номер телефона', required=False, validators=[
        validators.RegexValidator(
            regex=r'^(\+7|8)?(?(1) ?)((\()|(\-))?\d{3}(?(2)(?(3)\))(?(4)\-)) ?\d{3}( |\-)?\d{2}( |\-)?\d{2}$')])

    class Meta:
        model = HoHooUser
        fields = (
            'username',
            'email',
            'phone',
            'last_name',
            'first_name',
            'middle_name',
            'userpic',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserUpdateForm(UserChangeForm):
    phone = forms.CharField(label='Номер телефона', required=False, validators=[
        validators.RegexValidator(
            regex=r'^(\+7|8)?(?(1) ?)((\()|(\-))?\d{3}(?(2)(?(3)\))(?(4)\-)) ?\d{3}( |\-)?\d{2}( |\-)?\d{2}$')])

    class Meta:
        model = HoHooUser
        fields = (
            'username',
            'email',
            'phone',
            'last_name',
            'first_name',
            'middle_name',
            'userpic',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = forms.HiddenInput()
