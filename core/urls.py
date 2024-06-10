from . import views;
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('helpcenter', views.helpcenter, name='helpcenter'),
    path('tracking', views.tracking, name='tracking'),
    path('contactform', views.contactform, name='contactform'),
    path('whoweare', views.whoweare, name='whoweare'),
    path('terms', views.terms, name='terms'),
    path('ppolicy', views.ppolicy, name='ppolicy'),
    path('my-orders/', views.userdetails, name='userdetails'),
    path('my-orders/<uuid:id>/', views.userhistory, name='userhistory'),
    





]