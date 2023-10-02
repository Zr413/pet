from django_filters import DateFilter, FilterSet, AllValuesFilter
from django.forms import DateInput
from .models import News


# Создаем свой набор фильтров для модели News.
class NewsFilter(FilterSet):
    time = DateFilter(
        field_name='time',
        lookup_expr='icontains',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        ),
    )
    article_or_news = AllValuesFilter()

    class Meta:
        model = News
        fields = {'title': ['icontains']}
