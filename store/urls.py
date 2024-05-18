from . import views;
from django.urls import path

urlpatterns = [
    path('', views.products, name='store'),
    path('<uuid:id>', views.details, name='details')
]