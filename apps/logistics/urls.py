from django.urls import path
from . import views

app_name = 'logistics'

urlpatterns = [
    path('', views.logistics_list, name='list'),
    path('<int:pk>/', views.logistics_detail, name='detail'),
] 