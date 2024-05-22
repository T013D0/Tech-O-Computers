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
    path('administration/graphics/', views.graphics, name='dash-graphics'),
    path('administration/processor/', views.processor, name='dash-processor'),
    path('administration/ram/', views.ram, name='dash-ram'),
    path('administration/storage/', views.storage, name='dash-storage'),
    path('administration/screen/', views.screen, name='dash-screen'),




]