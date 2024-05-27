from . import views;
from django.urls import path

urlpatterns = [
    path('store/', views.products, name='store'),
    path('store/<uuid:id>', views.details, name='details'),
    path('update_item/', views.updateItem, name='update_item'),
    path('cart/', views.cart, name='cart'),
]