from django.urls import path
from . import views

urlpatterns = [
    path('login-sylvia/', views.login_sylvia, name='login_sylvia'),  
    path('', views.login_inicial, name='login_inicial'),  
    ]