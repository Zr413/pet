import logging
from datetime import datetime

import django_filters
import pytz  # Импортируем стандартный модуль для работы с часовыми поясами
from celery import shared_task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .filters import NewsFilter
from .forms import NewsForm
from .models import News, Categories, Author

logger = logging.getLogger(__name__)

from blog.serializers import *


# Вывод списка новостей и статей
class NewsList(ListView):
    model = News
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'articleviews'
    paginate_by = 4

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['next_sale'] = None
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Вывод статьи или новости
class NewsDetail(DetailView):
    logger.info("INFO")

    model = News
    template_name = 'new.html'
    context_object_name = 'art_views'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Создание новости
class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    logger.info("INFO")

    permission_required = ('blog.add_news',)
    raise_exception = True
    form_class = NewsForm
    model = News
    template_name = 'news_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form) and HttpResponseRedirect('/article/')

    def create_news(request):
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/article/')

        return render(request, 'news_create.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Обновление новости
class NewsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    logger.info("INFO")

    permission_required = ('blog.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form) and HttpResponseRedirect('/article/id/')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.author == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Удаление новости
class NewsDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    logger.info("INFO")

    permission_required = ('blog.delete_news',)
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.author == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Поиск по полям статей и новостей
class NewsSearch(ListView):
    logger.info("INFO")

    model = News
    template_name = 'news_search.html'
    context_object_name = 'articlesearch'
    ordering = ['-time']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Создание статьи
class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    logger.info("INFO")

    permission_required = ('blog.add_news',)
    raise_exception = True
    form_class = NewsForm
    model = News
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        form.instance.article_or_news = News.ARTICLE
        return super().form_valid(form) and HttpResponseRedirect('/article/')

    def create_article(request):
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/article/')

        return render(request, 'article_create.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Обновление статьи
class ArticleUpdate(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    logger.info("INFO")

    permission_required = ('blog.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'article_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form) and HttpResponseRedirect('/article/')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.author == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Удаление статьи
class ArticleDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    logger.info("INFO")

    permission_required = ('blog.delete_news',)
    model = News
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.author == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Вывод всех категорий по выбранному значению
class CategoriListView(ListView):
    logger.info("INFO")

    model = News
    template_name = 'categori_list.html'
    context_object_name = 'categori_news_list'

    def get_queryset(self):
        self.new_cat = get_object_or_404(Categories, id=self.kwargs['pk'])
        queryset = News.objects.filter(new_cat=self.new_cat).order_by('-time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.new_cat.subscribes.all()
        context['new_cat'] = self.new_cat
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Подписка на выбранную категорию новостей
# @login_required
# def subscrib(request, pk):
#     user = request.user
#     subscribes = Categories.objects.get(id=pk)
#     subscribes.subscribes.add(user)
#
#     message = 'Вы успешно подписались на категорию'
#     return render(request, 'subscribe.html', {'categori': subscribes, 'message': message})


@login_required
@csrf_protect
def subscriptions(request, action=None, pk=None):
    if action and pk:
        category = Categories.objects.get(id=pk)

        if action == 'subscribe':
            Subscription.objects.get_or_create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category).delete()

    categories = Categories.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('title')

    return render(request, 'subscribe.html', {'categories': categories})

# def subscriptions(request, action, pk):
#     category = Categories.objects.get(id=pk)
#
#     if action == 'subscribe':
#         Subscription.objects.create(user=request.user, category=category)
#     elif action == 'unsubscribe':
#         Subscription.objects.filter(
#             user=request.user,
#             category=category,
#         ).delete()
#
#     categories_with_subscriptions = Categories.objects.annotate(
#         user_subscribed=Exists(
#             Subscription.objects.filter(
#                 user=request.user,
#                 category=OuterRef('pk'),
#             )
#         )
#     ).order_by('name')
#     return render(
#         request,
#         'subscribe.html',
#         {'categories': categories_with_subscriptions},
#     )


class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = News.objects.all()
        auth_id = self.request.query_params.get('auth_id', None)
        news_id = self.request.query_params.get('news_categories', None)
        if auth_id is not None:
            queryset = queryset.filter(author_id=auth_id)
        if news_id is not None:
            queryset = queryset.filter(new_cat=news_id)
        return queryset


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().filter(is_active=True)
    serializer_class = UserSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["username", "email", "password"]


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all().filter(is_active=True)
    serializer_class = AuthorSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["full_name", ]

    def destroy(self, request, pk, format=None):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesViewset(viewsets.ModelViewSet):
    queryset = Categories.objects.all().filter(is_active=True)
    serializer_class = CategoriesSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["title", ]

    def destroy(self, request, pk, format=None):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetList(APIView):
    @swagger_auto_schema(
        operation_description='Get',
        responses={200: 'OK'},
    )
    def get(self, request):
        ob = News.objects.all()
        return Response(ob, status=status.HTTP_200_OK)
