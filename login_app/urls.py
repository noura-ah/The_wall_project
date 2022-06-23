from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index),
    path('wall',views.success,name='success'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('delete',views.delete,name='delete'),
]