from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
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
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
            messages.success(request, ("O as informações do teu perfil foram atualizadas!."))
            return redirect('home')
        
        return render(request, 'update_info.html', {'form':form})
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
                messages.success(request, "A tua password foi alterada!.")
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
        messages.success(request, "Tens de entrar na tua conta para veres isto!.")
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
    
