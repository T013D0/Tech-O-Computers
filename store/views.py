from django.shortcuts import render, redirect
from .models import Product, Notebook, Computer, AllInOne, Brand
from django.core.paginator import Paginator

# Create your views here.
def products(request):
    products = Product.objects.all().filter(stock__gt=0)
    brands =  Brand.objects.all()
    type = request.GET.get("type")
    if type != "" or type is not None:
        match(type):
            case "desktop":
                products = Computer.objects.all().filter(stock__gt=0)
            case "notebooks":
                products = Notebook.objects.all().filter(stock__gt=0)
            case "all-in-one":
                products = AllInOne.objects.all().filter(stock__gt=0)
    paginator = Paginator(products, 25)
    page = request.GET.get('page')
    if page is None or page == "":
        page = 1
    context = { "products": paginator.get_page(page).object_list, "page_obj": paginator.get_page(page), "per_page": paginator.per_page, "total": products.count(), "brands": brands}
    return render(request, 'store/products.html', context)

def details(request, id):
    product = Product.objects.get(id=id)
    if product is None:
        return redirect('store')
    

    if Notebook.objects.filter(id=id).exists():
        product = Notebook.objects.get(id=id)
    elif Computer.objects.filter(id=id).exists():
        product = Computer.objects.get(id=id)
    elif AllInOne.objects.filter(id=id).exists():
        product = AllInOne.objects.get(id=id)
    context = { "product": product}
    return render(request, 'store/details.html', context)