from django.shortcuts import render
from store.models import Product


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

def error_500(request):
    return render(request, 'core/500.html', status=500)

def error_403(request, exception):
    return render(request, 'core/403.html', status=403)