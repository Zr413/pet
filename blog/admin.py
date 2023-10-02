from django.contrib import admin
from .models import Categories, News, Author, Comment

from modeltranslation.admin import \
    TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


# Register your models here.

# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Categories


class NewsAdmin(TranslationAdmin):
    model = News


admin.site.register(Categories)
admin.site.register(News)
admin.site.register(Author)
admin.site.register(Comment)
