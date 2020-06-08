""" authapp views
"""
from hashlib import sha1
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic.edit import FormView, UpdateView, CreateView
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserVerifyForm
from .models import HoHooUser, Token

# Create your views here.

@login_required
def index(request):
    """ user profile view
    """
    context = {'page_title': 'Профиль пользователя ' + request.user.username}
    context['content_header'] = context['page_title']
    context['object'] = HoHooUser.objects.get(username=request.user.username)
    return render(request, 'authapp/user_detail.html', context)


class UserLoginView(FormView):
    """ user login view
    """
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('authapp:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Авторизация'
        context['content_header'] = 'Вход для зарегистрированных пользователей'
        return context

    def form_valid(self, form):
        user = None
        try:
            user = HoHooUser.objects.get(username=form.cleaned_data['username'])
        except HoHooUser.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('authapp:login'))
        if user.is_active:
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(self.request, user)
            return super().form_valid(form)
        return HttpResponseRedirect(reverse(
            'authapp:verify_form', kwargs={'username': user.username}))


def user_logout(request):
    """ user logout
    """
    logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    """ user profile edit view
    """
    template_name = 'authapp/user_update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('authapp:index')

    def get_object(self, queryset=None):
        return HoHooUser.objects.get(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактирование данных пользователя ' + self.request.user.username
        context['content_header'] = context['page_title']
        return context


class UserRegisterView(CreateView):
    """ new user registration view
    """
    template_name = 'authapp/signup.html'
    form_class = UserRegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Регистрация'
        context['content_header'] = 'Регистрация нового пользователя'
        return context

    def get_success_url(self):
        user = self.object
        user.is_active = False
        code = sha1(user.username.encode('utf-8'))
        code.update(str(now()).encode('utf-8'))
        code = code.hexdigest()
        user.token = Token(code=code)
        user.token.save()
        user.save()
        subj = 'Рога и Копыта - Подтверждение регистрации'
        msg = render_to_string(
            'email/user_verify.html',
            {'token': user.token, 'user': user, 'host_name': settings.HOST_NAME})
        mailfrom = settings.DEFAULT_FROM_EMAIL
        mailto = (user.email,)
        send_mail(
            subj, msg, mailfrom, mailto,
            fail_silently=True, html_message=msg)
        return reverse(
            'authapp:verify_form', kwargs={'username': self.object.username})


def user_verify(request, code=None, username=None):
    if code:
        try:
            token = Token.objects.get(code=code)
        except Token.DoesNotExist:
            token = None
        except Token.MultipleObjectsReturned:
            Token.objects.filter(code=code).delete()
            token = None
    else:
        if request.method == "POST":
            code = request.POST.get('code', None)
            try:
                token = Token.objects.get(code=code)
            except Token.DoesNotExist:
                token = None
        else:
            try:
                user = HoHooUser.objects.get(username=username)
            except HoHooUser.DoesNotExist:
                return HttpResponseRedirect(reverse('authapp:login'))
            if user.is_active:
                return HttpResponseRedirect(reverse('authapp:login'))
            form = UserVerifyForm()
            context = {
                'page_title': 'Завершение регистрации: подтверждение адреса Email',
                'content_header': 'Для завершения регистрации введите код',
                'form': form,
                'user': user,
            }
            return render(request, 'authapp/verify_form.html', context)
    if token and token.is_valid():
        user = token.user
        if username and username != user.username:
            # something extremely wrong happened
            # here must be a cool code to kick that lying ass
            pass
        elif not user.is_active:
            user.is_active = True
        token.delete()
        user.save()
    return HttpResponseRedirect(reverse('authapp:login'))
    # here can be a code to renew activation token
