from . import views;
from django.urls import path

urlpatterns = [
    path('', views.all_products, name='store'),
]