""" forms for register, update and login user
"""
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.core import validators
from .models import HoHooUser, Token, UserProfile


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

    def confirm_login_allowed(self, user):
        pass


class UserRegisterForm(UserCreationForm):
    required_css_class = 'required'

    phone = forms.CharField(label='Номер телефона', required=False, validators=[
        validators.RegexValidator(
            regex=r'^(\+7|8)?(?(1) ?)((\()|(\-))?\d{3}(?(2)(?(3)\))(?(4)\-)) ?\d{3}( |\-)?\d{2}( |\-)?\d{2}$')])
    email = forms.EmailField(label='Адрес электронной почты', required=True)

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

    def clean_email(self):
        email = self.cleaned_data['email']
        if HoHooUser.objects.filter(email=email):
            raise forms.ValidationError(
                'Этот адрес электронной почты уже зарегистрирован')
        return email


class UserUpdateForm(UserChangeForm):
    required_css_class = 'required'

    phone = forms.CharField(label='Номер телефона', required=False, validators=[
        validators.RegexValidator(
            regex=r'^(\+7|8)?(?(1) ?)((\()|(\-))?\d{3}(?(2)(?(3)\))(?(4)\-)) ?\d{3}( |\-)?\d{2}( |\-)?\d{2}$')])
    email = forms.EmailField(label='Адрес электронной почты', required=True)

    class Meta:
        model = HoHooUser
        fields = (
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.fields['email'].has_changed(email, self.initial['email']):
            if HoHooUser.objects.filter(email=email):
                raise forms.ValidationError(
                    'Этот адрес электронной почты использован в другом аккаунте')
        return email


class UserVerifyForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Token
        fields = ('code',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserProfileEditForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = UserProfile
        fields = ('payment', 'address',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
