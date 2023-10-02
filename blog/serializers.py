from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, value):
        return value.title

    class Meta:
        model = Categories
        fields = ['id', 'title', ]


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    new_cat = CategoriesSerializer(many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'article', 'article_or_news', 'new_cat', ]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'full_name', 'user']
        lookup_field = 'user'
