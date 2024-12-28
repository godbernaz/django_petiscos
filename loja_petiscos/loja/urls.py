from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre-mim/', views.about_me, name='about_me'),
    path('inciar-sessao/', views.login_user, name='login'),
    path('terminar-sessao/', views.logout_user, name='logout'),
    path('registar/', views.register_user, name='register'),
    path('editar-password/', views.update_password, name='update_password'),
    path('editar-perfil/', views.update_user, name='update_user'),
    path('editar-info/', views.update_info, name='update_info'),
    path('produto/<int:pk>', views.about_product, name='about_product'),
    path('categoria/<str:foo>', views.category, name='category'),
    path('procurar/', views.search, name='search'),
    path('testes/', views.home_testes, name='home_testes'),
    path('politica-privacidade/', views.privacy_policy, name='privacy_policy'),
    path('termos-condicoes/', views.terms_conditions, name='terms_conditions'),
]