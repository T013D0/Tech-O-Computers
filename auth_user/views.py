from django.shortcuts import render, redirect
from django.contrib import messages
from auth_user.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def login(request):

    if request.method == 'POST':
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Bienvenido')
            return redirect('index')
        else:
            messages.error(request, 'Email o Contraseña incorrectos')
            return redirect('login')
    return render(request, 'auth_user/login.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rut = request.POST.get('rut')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'auth_user/register.html')
        
        if User.objects.filter(rut=rut).exists():
            messages.error(request, 'El rut ya se encuentra registrado')
            return render(request, 'auth_user/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya se encuentra registrado')
            return render(request, 'auth_user/register.html')
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name, rut=rut, email=email, password=password)
        user.save()
        messages.success(request, 'Usuario registrado correctamente')
        return redirect('login')
    return render(request, 'auth_user/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'auth_user/admin/dashboard.html')