from . import views;
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.logout_view, name="logout"),
    path("accounts/<uidb64>/<token>/", views.activate, name="activate"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='auth_user/resetpassword.html', html_email_template_name='auth_user/emails/passemail.html', extra_email_context={'title': 'Cambio de contraseña'}), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='auth_user/passwordresetsend.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth_user/passwordresetform.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_user/passwordresetcomplete.html'), name='password_reset_complete'),
    path("accounts/<uidb64>/<token>/", views.activate, name="activate"),
    path('administration/dashboard/', views.dashboard, name='dashboard'),
    path('administration/products/', views.list_products, name='dash-list-products'),
    path('administration/products/<uuid:id>/', views.editproduct, name='dash-editproduct'),
    path("administration/products/remove/<uuid:id>/", views.removeproduct, name="dash-removeproduct"),
    path('administration/orders/', views.orders, name='dash-orders'),
    path('administration/orders/<uuid:id>/', views.orderdetail, name='dash-detailorder'),
    path('administration/ordersusers/<str:id>/', views.userorders, name='dash-ordersusers'),
    path('administration/packages/', views.packages, name='dash-packages'),
    path('administration/transactions/', views.transactions, name='dash-transactions'),
    path('administration/users/', views.users, name='dash-users'),
    path('administration/brands/', views.brands, name='dash-brands'),
    path('administration/brands/add/', views.addbrand, name='dash-addbrand'),
    path('administration/brands/remove/<uuid:id>/', views.removebrand, name='dash-removebrand'),
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
    path("administration/users/remove/<str:id>/", views.removeuser, name="dash-removeuser"),
    path("administration/editusers/<str:id>/", views.edituser, name="dash-edituser"),
    path("administration/removeorder/<uuid:id>/", views.removeOrder, name="dash-removeorder"),

    


    path('api/order/', views.editDeliveryStatus),
]