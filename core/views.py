from django.shortcuts import render
from store.models import Product

# Create your views here.
def index(request):
    top_prods = Product.objects.all().filter(stock__gt=0).order_by('price')[:3]
    context = { 'top_prods': top_prods }
    return render(request, 'core/index.html', context)
