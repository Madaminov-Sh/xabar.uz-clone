from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from news import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_page'),
    path('contact/', views.ContactView.as_view(),name='contact_page'),
    path('create/', views.PostCreateView.as_view(),name='post_create_page'),
    path('adminpage/', views.AdminPageView.as_view(), name='admin_page'),
    path('search/', views.SearchResultView.as_view(), name='post_search_page'),
    path('detail/<slug:slug>/', views.detailview, name='post_detail_page'),
    path('delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post_delete_page'),
    path('update/<slug:slug>/', views.PostUpdateView.as_view(), name='post_update_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)