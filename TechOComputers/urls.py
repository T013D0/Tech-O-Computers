"""
URL configuration for TechOComputers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from store.views import commit_pay, webpay_plus_create, deliveryPost

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('store.urls')),
    path('', include('auth_user.urls')),
    path('webpay-plus-create/', webpay_plus_create),
    path('shipping/', deliveryPost),
    path('webpay-plus-create/commitpay/', commit_pay, name='commit_pay'),
]

handler404 = 'core.views.error_404'
