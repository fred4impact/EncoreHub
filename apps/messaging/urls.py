from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.message_list, name='list'),
    path('<int:pk>/', views.message_detail, name='detail'),
] 