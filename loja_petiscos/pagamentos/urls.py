from django.urls import path
from . import views

urlpatterns = [
    path('pagamento_sucesso', views.payment_success, name='payment_success'),
    path('pagamento', views.checkout, name='checkout'),
    path('detalhes_pagamento', views.billing_info, name='billing_info'),
    path('processar_pedido', views.process_order, name='process_order'),
    path('pedidos_finalizados', views.shipped_dash, name='shipped_dash'),
    path('pedidos_inacabados', views.not_shipped_dash, name='not_shipped_dash'),
    path('pedidos/<int:pk>', views.orders, name='orders'),
]
