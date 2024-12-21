from django.shortcuts import render, get_object_or_404
from .cart import Cart
from loja.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages import get_messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    return render(request, 'cart_summary.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals})

def cart_add(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        product = get_object_or_404(Product, id=product_id)
        
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()

        # Adiciona mensagem ao sistema de mensagens
        messages.success(request, "Produto adicionado ao seu carrinho!")
        
        # Captura as mensagens e envia no JSON
        storage = get_messages(request)
        message_list = [{'level': message.level, 'message': message.message} for message in storage]

        return JsonResponse({'qty': cart_quantity, 'messages': message_list})
        
        
def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)
        
        response = JsonResponse({'product':product_id})
        messages.success(request, ("O produto foi removido do carrinho com sucesso!"))
        return response

def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("A quantidade foi alterada com sucesso!."))
        return response