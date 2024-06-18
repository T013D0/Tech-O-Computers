from django.shortcuts import render, redirect
from store.models import Product
from auth_user.models import User
from store.models import Product, Notebook, Computer, AllInOne, Brand, Recipe, RecipeDetails, Delivery, Payment
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q




# Create your views here.
def index(request):
    top_prods = Product.objects.all().filter(stock__gt=0).order_by('price')[:2]
    context = { 'top_prods': top_prods }
    return render(request, 'core/index.html', context)

def helpcenter(request):
    return render(request, 'core/footer/helpcenter.html')

def contactform(request):
    return render(request, 'core/footer/contactform.html')

def ppolicy(request):
    return render(request, 'core/footer/ppolicy.html')

def terms(request):
    return render(request, 'core/footer/terms.html')

def tracking(request):
    return render(request, 'core/footer/tracking.html')

def whoweare(request):
    return render(request, 'core/footer/whoweare.html')

def error_404(request, exception):
    return render(request, 'core/404.html', status=404)

@login_required
def userdetails(request):
    user = request.user
    orders = Recipe.objects.filter(complete=True, client=user).all()

    orderByDate = request.GET.get('orderByDate')
    if orderByDate is not None:
        if orderByDate == 'asc':
            orders = orders.order_by('created_at')
        elif orderByDate == 'desc':
            orders = orders.order_by('-created_at')

    context = {'user_orders': orders, 'user': user}
    return render(request, 'core/userdetails.html', context)

@login_required
def profile(request):

    if request.method == 'POST':
        user = request.user
        
        if User.objects.filter(email=request.POST.get('email')).exclude(rut=user.rut).exists():
            messages.error(request, 'El email ya está en uso')
            return redirect('profile')
        
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Perfil actualizado')
        return redirect('profile')
    
    last_recipes = Recipe.objects.filter(client=request.user, complete=True).order_by('-created_at')[:5]
    context = {'last_recipes': last_recipes}
    return render(request, 'core/profile.html', context)

@login_required
def userhistory(request, id):

    order = Recipe.objects.get(id=id)

    if order is None:
        messages.error(request, 'La orden no existe')
        return redirect('userdetails')
    
    if request.user != order.client:
        raise PermissionDenied
    
    details = RecipeDetails.objects.filter(recipe=order).all()
    context = {'order' : order, 'details': details}
    return render(request, 'core/userhistory.html', context)

def error_500(request):
    return render(request, 'core/500.html', status=500)

def error_403(request, exception):
    return render(request, 'core/403.html', status=403)