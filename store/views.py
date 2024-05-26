from django.shortcuts import render, redirect
from .models import Product, Notebook, Computer, AllInOne, Brand, Recipe, RecipeDetails
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

# Create your views here.

#Global variables
def cart_data(request):
    if request.user.is_authenticated:
        recipe, created = Recipe.objects.get_or_create(client=request.user, complete=False)
        items = recipe.recipedetails_set.all()
        cartItems = recipe.get_cart_items
    else:
        items = []
        recipe = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = recipe['get_cart_items']
    return {'cartItems': cartItems, 'items': items, 'recipe': recipe}

def products(request):
    products = Product.objects.all().filter(stock__gt=0)
    brands =  Brand.objects.all()
    type = request.GET.get("type")
    if type != "" and type is not None:
        match(type):
            case "desktop":
                products = Computer.objects.all().filter(stock__gt=0)
            case "notebooks":
                products = Notebook.objects.all().filter(stock__gt=0)
            case "all-in-one":
                products = AllInOne.objects.all().filter(stock__gt=0)

    name = request.GET.get("search")
    if name != "" and name is not None:
        products = products.filter(name__icontains=name)
    
    orderBy = request.GET.get("orderBy")
    if orderBy != "" and orderBy is not None:
        match(orderBy):
            case "revelance":
                products = products
            case "minor-mayor":
                products = products.order_by("price")
            case "mayor-minor":
                products = products.order_by("-price")

    brandp = request.GET.get("brand")
    if brandp != "" and brandp is not None:
        if Brand.objects.filter(name=brandp).exists():
            brand = Brand.objects.get(name=brandp)
            products = products.filter(brand=brand)

    price = request.GET.get("price")
    if price != "" and price is not None:
        filter_price = price.split("-")
        if len(filter_price) == 2:
            products = products.filter(price__range=(int(filter_price[0]), int(filter_price[1])))
    
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

def updateItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('ProductId:', productId)

    product = Product.objects.get(id=productId)
    recipe, created = Recipe.objects.get_or_create(client=request.user, complete=False)

    recipeDetails, created = RecipeDetails.objects.get_or_create(recipe=recipe, product=product)

    if action == 'add':
        recipeDetails.quantity = (recipeDetails.quantity + 1)
    elif action == 'remove':
        recipeDetails.quantity = (recipeDetails.quantity - 1)
    elif action == 'delete':
        recipeDetails.quantity = 0

    recipeDetails.save()

    if recipeDetails.quantity <= 0:
        recipeDetails.delete()
    

    return JsonResponse('Item was added', safe=False)

def cart(request):
    data = cart_data(request)
    items = data['items']
    recipe = data['recipe']
    context = { "items": items, "recipe": recipe}
    return render(request, 'store/cart.html', context)