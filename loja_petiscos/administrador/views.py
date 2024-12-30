from django.shortcuts import render, redirect
from loja.models import Profile, Product, Category, Customer, Product
from pagamentos.models import Order, OrderItem
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator

def pedidos_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Obter todos os pedidos
        orders = Order.objects.all()

        p_orders = Paginator(Order.objects.all(), 10)
        page_orders = request.GET.get('page')
        ordersp = p_orders.get_page(page_orders)
    
        # Processar pedidos do formulário
        if request.method == "POST":
            status = request.POST['shipping_status'] == 'true'  # Converte para booleano
            num = request.POST['num']
            now = datetime.datetime.now()
            
            # Atualizar o estado do pedido
            order = Order.objects.filter(id=num)
            if order.exists():
                order.update(shipped=status, date_shipped=now)
                messages.success(request, "Shipping Status Updated")
            else:
                messages.error(request, "Order not found")
            
            return redirect('pedidos_dashboard')  # Redireciona para evitar reenvio do formulário

        # Separar pedidos finalizados e inacabados
        finished_orders = orders.filter(shipped=True)[:5]
        unfinished_orders = orders.filter(shipped=False)[:5]

        # Renderizar o template com os dois grupos de pedidos
        return render(request, 'pedidos_dashboard.html', {
            'finished_orders': finished_orders,
            'unfinished_orders': unfinished_orders,
            'ordersp': ordersp
        })
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Obter todos os pedidos
        orders = Order.objects.all()

        # Processar pedidos do formulário
        if request.method == "POST":
            status = request.POST['shipping_status'] == 'true'  # Converte para booleano
            num = request.POST['num']
            now = datetime.datetime.now()
            
            # Atualizar o estado do pedido
            order = Order.objects.filter(id=num)
            if order.exists():
                order.update(shipped=status, date_shipped=now)
                messages.success(request, "Shipping Status Updated")
            else:
                messages.error(request, "Order not found")
            
            return redirect('admin_dashboard')  # Redireciona para evitar reenvio do formulário

        # Separar pedidos finalizados e inacabados
        finished_orders = orders.filter(shipped=True)
        unfinished_orders = orders.filter(shipped=False)

        # Renderizar o template com os dois grupos de pedidos
        return render(request, 'admin_dashboard.html', {
            "finished_orders": finished_orders,
            "unfinished_orders": unfinished_orders
        })
    else:
        messages.error(request, "Access Denied")
        return redirect('home')