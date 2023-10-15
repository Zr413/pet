from django.contrib import admin
from .models import Categories, News, Author, Comment

from modeltranslation.admin import \
    TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


def nullfy_quantity(modeladmin, request, queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(quantity=0)
    modeladmin.nullfy_quantity.short_description = 'Обнулить товары'  # описание для более понятного представления в админ панеле задаётся, как будто это объект


class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'article')  # оставляем только имя и цену товара
    list_filter = ('title', 'article')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('article_or_news', 'author', 'new_cat')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_quantity]


# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Categories


class NewsAdmin(TranslationAdmin):
    model = News
    # list_display = [field.name for field in News._meta.get_fields()]


admin.site.register(Categories)
admin.site.register(News, ProductAdmin)
admin.site.register(Author)
admin.site.register(Comment)
