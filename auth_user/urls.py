from . import views;
from django.urls import path

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('administration/dashboard/', views.dashboard, name='dashboard'),
    path('administration/products/', views.list_products, name='dash-list-products'),
    path('administration/products/<uuid:id>/', views.editproduct, name='dash-editproduct'),
    path("administration/products/remove/<uuid:id>/", views.removeproduct, name="dash-removeproduct"),
    path('administration/orders/', views.orders, name='dash-orders'),
    path('administration/orders/<uuid:id>/', views.orderdetail, name='dash-detailorder'),
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
    path('administration/components/add/<str:type>', views.addcomponent, name='dash-addcomponent'),
    path('administration/components/edit/<str:type>/<uuid:id>', views.editComponent, name='dash-editcomponent'),
    path('administration/components/remove/<str:type>/<uuid:id>', views.removeComponent, name='dash-removecomponent'),
    path('api/order/', views.editDeliveryStatus),

]