from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from blog import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewset)
router.register(r'user', views.UserViewset)
router.register(r'author', views.AuthorViewset)
router.register(r'categories', views.CategoriesViewset)

schema_view = get_schema_view(
    openapi.Info(
        title="Your API title",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(),
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('blog.urls')),
    path('article/', include('blog.urls')),
    path("accounts/", include("allauth.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(router.urls), name='api')
]
