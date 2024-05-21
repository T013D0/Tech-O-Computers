from django.shortcuts import render, redirect
from django.contrib import messages
from auth_user.models import User
from store.models import Product, Brand
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from store.models import Product, Notebook, Computer, AllInOne, Brand, Recipe, RecipeDetails
from django.db.models import Sum, F, IntegerField

# Create your views here.
def login(request):

    if request.method == 'POST':
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Bienvenido ' + user.first_name + ' ' + user.last_name + '!')

            next = request.GET.get('next')
            if next is not None and next != '':
                return redirect(next)
            else:
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
@permission_required('auth_user.view_user')
def dashboard(request):
    count_products = Product.objects.all().count()
    count_sell = Recipe.objects.all().count()
    profit = RecipeDetails.objects.all().aggregate(profit=Sum(F('product__price') * F('quantity'), output_field=IntegerField()))['profit']
    data = []
    for i in range(1, 13):
        data.append(Recipe.objects.filter(created_at__month=i).count())

    products = Product.objects.all()
    context = { "count_products": count_products, "count_sell": count_sell, "profit": profit, "data": data, "products": products}
    return render(request, 'auth_user/admin/dashboard.html', context)

@login_required
@permission_required('auth_user.view_user')
def orders(request):
    return render(request, 'auth_user/admin/orders.html')

@login_required
@permission_required('auth_user.view_user')
def packages(request):
    return render(request, 'auth_user/admin/packages.html')

@login_required
@permission_required('auth_user.view_user')
def transactions(request):
    return render(request, 'auth_user/admin/transactions.html')

@login_required
@permission_required('auth_user.view_user')
def list_products(request):
    products = Product.objects.all()
    brands =  Brand.objects.all()
    type = request.GET.get("type")
    if type != "" and type is not None:
        match(type):
            case "desktop":
                products = Computer.objects.all()
            case "notebooks":
                products = Notebook.objects.all()
            case "all-in-one":
                products = AllInOne.objects.all()

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
    
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    if page is None or page == "":
        page = 1

    context = { "products": paginator.get_page(page).object_list, "page_obj": paginator.get_page(page), "per_page": paginator.per_page, "total": products.count(), "brands": brands}
    return render(request, 'auth_user/admin/products/list.html', context)

@login_required
def users(request):
    user = User.objects.all()
    data = {'usuarios' : user}
    return render(request, 'auth_user/admin/users.html', data)