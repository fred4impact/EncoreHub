from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('complete-artist-profile/', views.complete_artist_profile, name='complete_artist_profile'),
    path('complete-venue-profile/', views.complete_venue_profile, name='complete_venue_profile'),
    path('complete-manager-profile/', views.complete_manager_profile, name='complete_manager_profile'),
    path('manager-verification/', views.manager_verification, name='manager_verification'),
    # Manager Discovery URLs
    path('managers/', views.manager_discovery, name='manager_discovery'),
    path('managers/<int:manager_id>/', views.manager_detail, name='manager_detail'),
] 