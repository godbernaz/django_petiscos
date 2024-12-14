from django.urls import path
from . import views

urlpatterns = [
    path('pagamento_sucesso/', views.payment_success, name='payment_success'),
]
