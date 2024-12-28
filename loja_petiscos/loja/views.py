from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from pagamentos.forms import ShippingForm
from pagamentos.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from carrinho.cart import Cart
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.paginator import Paginator
import random
from django.template.loader import render_to_string

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home_testes(request):
    pass
    '''desired_order = ['Entradas', 'Saladas', 'Carnes', 'Peixes', 'Tabuas', 'Tartes', 'Sobremesas']
    categories = sorted(
        Category.objects.all(),
        key=lambda x: desired_order.index(x.name) if x.name in desired_order else len(desired_order)
    )
    
    # Filtra os produtos por categoria, se o parâmetro existir
    category_id = request.GET.get('category')
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    # Paginação dos produtos
    p = Paginator(products, 4)
    page = request.GET.get('page', 1)

    try:
        product_page = p.page(page)
    except PageNotAnInteger:
        product_page = p.page(1)
    except EmptyPage:
        product_page = p.page(p.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/product_list.html', {'product_page': product_page})
        return JsonResponse({'html': html})

    return render(request, 'home_testes.html', {
        'categories': categories,
        'product_page': product_page
    })'''
    
def terms_conditions(request):
    return render(request, 'terms_conditions.html', {})

def privacy_policy(request):
    return render(request, 'privacy_policy.html', {})

def home(request):
    category_id = request.GET.get('category')
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    # Paginação dos produtos
    p = Paginator(products, 4)
    page = request.GET.get('page', 1)

    try:
        product_page = p.page(page)
    except PageNotAnInteger:
        product_page = p.page(1)
    except EmptyPage:
        product_page = p.page(p.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/product_list.html', {'product_page': product_page})
        return JsonResponse({'html': html})

    return render(request, 'home.html', {
        'product_page': product_page
    })

def about_me(request):
    return render(request, 'about_me.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']    
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            
            messages.success(request, ("Iníciaste sessão na tua conta com sucesso!."))
            return redirect('home')
        else:
            messages.error(request, ("Houve algum problema a entrar na tua conta, tenta novamente."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Saiste da tua conta!. Vemo-nos em breve."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1'] 
            
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Conta criada com sucesso, se quiseres termina de atualizar o teu perfil!."))
            return redirect('update_info')
        else:
            messages.error(request, ("Houve um problema com a criação da tua conta. Tenta novamente."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

def update_user(request):
    
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
        
            login(request, current_user)
            messages.success(request, ("O seu perfil foi atualizado!."))
            return redirect('home')
        
        return render(request, 'update_user.html', {'user_form':user_form})
    
    else:
        messages.error(request, ("Tens de iniciar sessão para alterares o teu perfil."))
        return redirect('home')
    
def update_info(request):
    
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            
            messages.success(request, ("O as informações do teu perfil foram atualizadas!."))
            return redirect('home')
        
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, ("Tens de iniciar sessão para alterares as informações do teu perfil."))
        return redirect('home')
        
def update_password(request):
    
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, ("A tua password foi alterada!."))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, ("Tens de entrar na tua conta para veres isto!."))
        return redirect('home')

def about_product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'about_product.html', {'product': product})

def category(request, foo):
    
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category}) 
    except:
        messages.error(request, ("A categoria que procuras não tem produtos disponiveis"))
        return redirect('home')
    
def search(request):
    
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched))
        
        if not searched:
            messages.error(request, ("A comida que procuras não existe ou não está disponível neste momento.."))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html', {})