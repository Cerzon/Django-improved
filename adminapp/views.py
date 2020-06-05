""" adminapp views
"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from authapp.forms import UserRegisterForm, UserUpdateForm
from authapp.models import HoHooUser
from mainapp.models import Category, Product

# Create your views here.


PRODUCT_LINKS = {
    'list': ('adminapp:product:list', 'К перечню товаров',),
    'create': ('adminapp:product:create', 'Создать новый',),
    'update': ('adminapp:product:update', 'Изменить',),
    'delete': ('adminapp:product:delete', 'Удалить',),
    'filter': ('adminapp:product:filter_list', 'По категории',),
}

USER_LINKS = {
    'list': ('adminapp:user:list', 'К списку пользователей',),
    'create': ('adminapp:user:create', 'Создать пользователя',),
    'update': ('adminapp:user:update', 'Изменить пользователя',),
    'delete': ('adminapp:user:delete', 'Удалить пользователя',),
}

CATEGORY_LINKS = {
    'list': ('adminapp:category:list', 'К списку категорий',),
    'create': ('adminapp:category:create', 'Создать категорию',),
    'update': ('adminapp:category:update', 'Изменить категорию',),
    'delete': ('adminapp:category:delete', 'Удалить категорию',),
}


def index(request):
    return HttpResponseRedirect(reverse('adminapp:user:list'))


class SuperUserPassesTestMixin(UserPassesTestMixin):
    """ check user is superuser
    """
    def test_func(self):
        return self.request.user.is_superuser


class UserListView(SuperUserPassesTestMixin, ListView):
    model = HoHooUser
    template_name = 'adminapp/object_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Пользователи',
            'content_header': 'Список пользователей',
            'links': USER_LINKS,
        })
        return context


class CreateUserView(SuperUserPassesTestMixin, CreateView):
    model = HoHooUser
    form_class = UserRegisterForm
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:user:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Добавление пользователя',
            'content_header': 'Список пользователей',
            'links': USER_LINKS,
            'submit_label': 'Сохранить',
        })
        return context


class UpdateUserView(SuperUserPassesTestMixin, UpdateView):
    model = HoHooUser
    form_class = UserUpdateForm
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:user:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Редактирование пользователя',
            'content_header': 'Изменение профиля ' + self.object.username,
            'links': USER_LINKS,
            'submit_label': 'Применить изменения',
        })
        return context


class DeleteUserView(SuperUserPassesTestMixin, DeleteView):
    model = HoHooUser
    template_name = 'adminapp/object_delete.html'
    success_url = reverse_lazy('adminapp:user:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Удаление пользователя',
            'content_header': 'Удаление профиля ' + self.object.username,
            'links': USER_LINKS,
        })
        return context


class CategoryListView(SuperUserPassesTestMixin, ListView):
    model = Category
    template_name = 'adminapp/object_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Категории',
            'content_header': 'Список категорий товаров',
            'links': CATEGORY_LINKS,
        })
        return context


class CreateCategoryView(SuperUserPassesTestMixin, CreateView):
    model = Category
    fields = '__all__'
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:category:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Добавление категории',
            'content_header': 'Добавить категорию товаров',
            'links': CATEGORY_LINKS,
            'submit_label': 'Сохранить',
        })
        return context


class UpdateCategoryView(SuperUserPassesTestMixin, UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:category:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Редактирование категории',
            'content_header': 'Изменить категорию ' + self.object.name,
            'links': CATEGORY_LINKS,
            'submit_label': 'Применить изменения',
        })
        return context


class DeleteCategoryView(SuperUserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'adminapp/object_delete.html'
    success_url = reverse_lazy('adminapp:category:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Удаление категории',
            'content_header': 'Удалить категорию ' + self.object.name,
            'links': CATEGORY_LINKS,
        })
        return context


class ProductListView(SuperUserPassesTestMixin, ListView):
    model = Product
    template_name = 'adminapp/object_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk', False):
            queryset = queryset.filter(category__pk=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update({
            'page_title': 'Товары',
            'content_header': 'Список товаров',
            'links': PRODUCT_LINKS,
            'filters': Category.objects.all()
        })
        if self.kwargs.get('pk', False):
            context['content_header'] += ' в категории "' + categories.get(
                pk=self.kwargs['pk']).name + '"'
        return context


class CreateProductView(SuperUserPassesTestMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:product:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Добавление товара',
            'content_header': 'Добавить товар',
            'links': PRODUCT_LINKS,
            'submit_label': 'Сохранить',
        })
        return context


class UpdateProductView(SuperUserPassesTestMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:product:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Редактирование товара',
            'content_header': 'Изменить товар ' + self.object.name,
            'links': PRODUCT_LINKS,
            'submit_label': 'Применить изменения',
        })
        return context


class DeleteProductView(SuperUserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'adminapp/object_delete.html'
    success_url = reverse_lazy('adminapp:product:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Удаление товара',
            'content_header': 'Удалиь товар ' + self.object.name,
            'links': PRODUCT_LINKS,
        })
        return context
