from . import views;
from django.urls import path

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('administration/dashboard/', views.dashboard, name='dashboard'),
    path('administration/products/', views.list_products, name='dash-list-products'),
    path('administration/orders/', views.orders, name='dash-orders'),
    path('administration/packages/', views.packages, name='dash-packages'),
    path('administration/transactions/', views.transactions, name='dash-transactions'),
    path('administration/users/', views.users, name='dash-users'),
    path('administration/brands/', views.brands, name='dash-brands'),
    path('administration/components/', views.components, name='dash-components'),
    path('administration/addproduct/', views.addproduct, name='dash-addproduct'),

]