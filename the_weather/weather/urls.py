from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('delete/<city_city_id>/', views.delete_city_id, name='delete_city_id'),
]
