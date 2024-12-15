from django.shortcuts import render, redirect
from carrinho.cart import Cart
from pagamentos.forms import ShippingForm, PaymentForm
from pagamentos.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from loja.models import Product, Profile
import datetime

def orders(request, pk):
    
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        
        if request.POST:
            status = request.POST['shipping_status']
            
            if status == 'true':
                order = Order.objects.filter(id=pk)
                order.update(shipped=True)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            
            messages.success(request, ("O estado do pedido foi alterado!"))
            return redirect('home')
                
        return render(request, 'payment/orders.html', {'order':order, 'items':items})
    else:
        messages.error(request, ("Acesso Negado!"))
        return redirect('home')    
        
def shipped_dash(request):
    
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
  
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			order = Order.objects.filter(id=num)
			now = datetime.datetime.now()
			order.update(shipped=False, date_shipped=now)
			
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def not_shipped_dash(request):
    
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
  
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			order = Order.objects.filter(id=num)
			now = datetime.datetime.now()
			order.update(shipped=True, date_shipped=now)
   
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'shipping_form':shipping_form})    
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'shipping_form':shipping_form})

def billing_info(request):
    
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
        
        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'shipping_form':shipping_form})
    else:
        messages.error(request, ("Acesso Negado!"))
        return redirect('home')

def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        phone = my_shipping['shipping_phone']

        # Create Shipping Address from session info
        shipping_address = (
            f"{my_shipping['shipping_address1']}\n"
            f"{my_shipping['shipping_address2']}\n"
            f"{my_shipping['shipping_city']}\n"
            f"{my_shipping['shipping_zipcode']}\n"
            f"{my_shipping['shipping_country']}"
        )
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # Logged in
            user = request.user
            # Create Order
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk

            # Get product info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                price = product.sale_price if product.is_sale else product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()

            # Delete the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")

            messages.success(request, "Order Placed!")
            return redirect('home')

        else:
            # Not logged in
            create_order = Order(
                full_name=full_name,
                email=email,
                phone=phone,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()

            # Add order items
            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()

            # Delete the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Order Placed!")
            return redirect('home')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})