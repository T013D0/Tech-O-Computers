from django.shortcuts import render

# Create your views here.
def products(request):
    types = ["desktop", "notebooks", "all-in-one"]
    products = {}
    type = request.GET.get("type")
    if type != "" or type is not None:
        match(type):
            case "desktop":
                products = {}
            case "notebooks":
                products = {}
            case "all-in-one":
                products = {}
    context = { "products": products }
    return render(request, 'store/products.html', context)