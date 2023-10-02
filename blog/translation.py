from blog.models import News, Categories
from modeltranslation.translator import register, \
    TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода

@register(Categories)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)  # указываем, какие именно поля надо переводить в виде кортежа


@register(News)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('title', 'article',)
