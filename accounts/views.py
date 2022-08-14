from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login as auth_login, authenticate, logout
from .models import User

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            user = User.objects.create_user(email, first_name, last_name)
            user.is_active=True
            user.set_password(password)
            user.save()
            return redirect('/')
        else:
            return render(request, 'accounts/add.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'accounts/add.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        auth_user = authenticate(request, username=email, password=password)
        if auth_user is not None:
            auth_login(request, auth_user)
            return redirect('/')
        else:            
            return redirect('register')    
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

def singout(request):
    logout(request)
    return redirect('/')



