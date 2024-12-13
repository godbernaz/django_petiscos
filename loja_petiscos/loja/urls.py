from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre-mim/', views.about_me, name='about_me'),
    path('inciar-sessao/', views.login_user, name='login'),
    path('terminar-sessao/', views.logout_user, name='logout'),
    path('registar/', views.register_user, name='register'),
]