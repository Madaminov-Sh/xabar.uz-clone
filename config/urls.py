from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
] + i18n_patterns (
    path('i18n/', include('django.conf.urls.i18n')),

    path('news/', include('news.urls', namespace='news')),
    path('register/', include('register.urls', namespace='register')),

    path('api/', include('news.api_urls.apiurls')),
    path('api/', include('register.api_urls.apiurls')),
)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)