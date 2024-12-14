from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

def home(request):
    products = Product.objects.all()[:8]  # Limitador inicial
    return render(request, 'home.html', {'products': products})

def about_me(request):
    return render(request, 'about_me.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']    
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
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
            messages.success(request, ("A tua conta foi criada com sucesso!."))
            return redirect('home')
        else:
            messages.error(request, ("Houve um problema com a criação da tua conta. Tenta novamente."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

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