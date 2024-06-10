from django.shortcuts import render, redirect
from store.models import Product
from auth_user.models import User
from store.models import Product, Notebook, Computer, AllInOne, Brand, Recipe, RecipeDetails, Delivery, Payment
from django.contrib import messages




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

def userdetails(request, id):
    user = User.objects.get(rut=id)
    orders = Recipe.objects.filter(complete=True, client=user ).all()
    context = {'orders' : orders, 'user': user}
    return render(request, 'core/userdetails.html', context)

def userhistory(request, id):
    order = Recipe.objects.get(id=id)

    if order is None:
        messages.error(request, 'La orden no existe')
        return redirect('userdetails')
    
    details = RecipeDetails.objects.filter(recipe=order).all()
    context = {'order' : order, 'details': details}
    return render(request, 'core/userhistory.html', context)

def error_500(request):
    return render(request, 'core/500.html', status=500)

def error_403(request, exception):
    return render(request, 'core/403.html', status=403)