from django.urls import path
from . import views

urlpatterns = [
    path('administrador-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('pedidos-dashboard/', views.pedidos_dashboard, name='pedidos_dashboard'),
]