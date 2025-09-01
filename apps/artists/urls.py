from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    # Artist discovery
    path('', views.artist_list, name='list'),
    path('<int:pk>/', views.artist_detail, name='detail'),
    
    # Portfolio management
    path('portfolio/', views.my_portfolio, name='my_portfolio'),
    path('portfolio/media/add/', views.add_media, name='add_media'),
    path('portfolio/media/<int:pk>/edit/', views.edit_media, name='edit_media'),
    path('portfolio/media/<int:pk>/delete/', views.delete_media, name='delete_media'),
    path('portfolio/performance/add/', views.add_performance, name='add_performance'),
    path('portfolio/performance/<int:pk>/edit/', views.edit_performance, name='edit_performance'),
    path('portfolio/performance/<int:pk>/delete/', views.delete_performance, name='delete_performance'),
    path('portfolio/availability/', views.manage_availability, name='manage_availability'),
    path('portfolio/availability/<int:pk>/edit/', views.edit_availability, name='edit_availability'),
    path('portfolio/availability/<int:pk>/delete/', views.delete_availability, name='delete_availability'),
    
    # API endpoints
    path('api/search/', views.artist_search_api, name='artist_search_api'),
    path('api/<int:artist_pk>/availability/', views.artist_availability_api, name='artist_availability_api'),
] 