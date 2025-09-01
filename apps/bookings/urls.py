from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Event management
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.edit_event, name='edit_event'),
    
    # Booking requests
    path('events/<int:event_pk>/request/', views.create_booking_request, name='create_booking_request'),
    path('artists/<int:portfolio_pk>/book/', views.create_artist_booking_request, name='create_artist_booking_request'),
    path('requests/', views.my_requests, name='my_requests'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/<int:pk>/respond/', views.respond_to_request, name='respond_to_request'),
    
    # Bookings
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    
    # API endpoints
    path('api/events/search/', views.event_search_api, name='event_search_api'),
] 