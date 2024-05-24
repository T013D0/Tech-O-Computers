from django.shortcuts import render, redirect
from django.contrib import messages
from auth_user.models import User
from store.models import Product, Brand, Ram, Storage, Processor, GraphicCard, Screen
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
def brands(request):
    brands = Brand.objects.all()
    context = {'brands' : brands}
    return render(request, 'auth_user/admin/products/brands.html', context)

@login_required
@permission_required('auth_user.view_user')
def graphics(request):
    graphics = GraphicCard.objects.all()
    context = {'graphics' : graphics}
    return render(request, 'auth_user/admin/products/graphics.html', context)

@login_required
@permission_required('auth_user.view_user')
def processor(request):
    processor = Processor.objects.all()
    context = {'processor' : processor}
    return render(request, 'auth_user/admin/products/processor.html', context)

@login_required
@permission_required('auth_user.view_user')
def ram(request):
    ram = Ram.objects.all()
    context = {'ram' : ram}
    return render(request, 'auth_user/admin/products/ram.html', context)

@login_required
@permission_required('auth_user.view_user')
def screen(request):
    screen = Screen.objects.all()
    context = {'screen' : screen}
    return render(request, 'auth_user/admin/products/screen.html', context)


@login_required
@permission_required('auth_user.view_user')
def storage(request):
    storage = Storage.objects.all()
    context = {'storage' : storage}
    return render(request, 'auth_user/admin/products/storage.html', context)


@login_required
@permission_required('auth_user.view_user')
def components(request):
    return render(request, 'auth_user/admin/products/components.html')

@login_required
@permission_required('auth_user.view_user')
def addproduct(request):

    brands = Brand.objects.all()
    screens = Screen.objects.all()
    processors = Processor.objects.all()
    graphics = GraphicCard.objects.all()
    rams = Ram.objects.all()
    storages = Storage.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        screen = request.POST.get('screen')
        type = request.POST.get('type')
        processor = request.POST.get('processor')
        graphic = request.POST.get('graphicscard')
        ram = request.POST.get('ram')
        storage = request.POST.get('storage')
        image = request.FILES.get('avatar')

        if Product.objects.filter(name=name).exists():
            messages.error(request, 'El producto ya se encuentra registrado')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        brnd = Brand.objects.get(id=brand)
        if brnd is None:
            messages.error(request, 'La marca no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        if type == "notebook" or type == "all-in-one":
            scrn = Screen.objects.get(id=screen)
            if scrn is None:
                messages.error(request, 'La pantalla no existe')
                return render(request, 'auth_user/admin/products/addproduct.html')

        ram_array = ram.split(",")

        rms = Ram.objects.all().filter(id__in=ram_array)
        if not rms.exists():
            messages.error(request, 'La memoria ram no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        prcsr = Processor.objects.get(id=processor)
        if prcsr is None:
            messages.error(request, 'El procesador no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        grphc = GraphicCard.objects.get(id=graphic)
        if grphc is None:
            messages.error(request, 'La tarjeta grafica no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        strg_array = storage.split(",")

        strg = Storage.objects.all().filter(id__in=strg_array)
        if not strg.exists():
            messages.error(request, 'El almacenamiento no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        if image is None:
            messages.error(request, 'La imagen es requerida')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        
        match (type):
            case "computer":
                product = Computer.objects.create(name=name, price=price, stock=stock, description=description, brand=brnd, processor=prcsr, graphicscard=grphc, image=image)
            case "notebook":
                product = Notebook.objects.create(name=name, price=price, stock=stock, description=description, brand=brnd, screen=Screen.objects.get(id=screen), processor=prcsr, graphicscard=grphc, image=image)
            case "all-in-one":
                product = AllInOne.objects.create(name=name, price=price, stock=stock, description=description, brand=brnd, screen=Screen.objects.get(id=screen), processor=prcsr, graphicscard=grphc, image=image)
        
        product.ram.set(rms)
        product.storage.set(strg)
        product.save()

        messages.success(request, f'Producto {product.name} registrado correctamente')
        return redirect('dash-list-products')
    
    context = {'brands': brands, 'screens': screens, 'processors': processors, 'graphics': graphics, 'rams': rams, 'storages': storages}

    return render(request, 'auth_user/admin/products/addproduct.html', context)

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
    context = {'usuarios' : user}
    return render(request, 'auth_user/admin/users.html', context)

@login_required
@permission_required('auth_user.view_user')
def editproduct(request, id):
    product = Product.objects.get(id=id)

    brands = Brand.objects.all()
    screens = Screen.objects.all()
    processors = Processor.objects.all()
    graphics = GraphicCard.objects.all()
    rams = Ram.objects.all()
    storages = Storage.objects.all()

    if product is None:
        messages.error(request, 'El producto no existe')
        return redirect('dash-list-products')
    
    
    if Notebook.objects.filter(id=id).exists():
        product = Notebook.objects.get(id=id)
    elif Computer.objects.filter(id=id).exists():
        product = Computer.objects.get(id=id)
    elif AllInOne.objects.filter(id=id).exists():
        product = AllInOne.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        screen = request.POST.get('screen')
        type = request.POST.get('type')
        processor = request.POST.get('processor')
        graphic = request.POST.get('graphicscard')
        ram = request.POST.get('ram')
        storage = request.POST.get('storage')
        image = request.FILES.get('avatar')

        if not Product.objects.filter(name=name).exists():
            messages.error(request, 'El producto no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        brnd = Brand.objects.get(id=brand)
        if brnd is None:
            messages.error(request, 'La marca no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        if type == "notebook" or type == "all-in-one":
            scrn = Screen.objects.get(id=screen)
            if scrn is None:
                messages.error(request, 'La pantalla no existe')
                return render(request, 'auth_user/admin/products/addproduct.html')

        ram_array = ram.split(",")

        rms = Ram.objects.all().filter(id__in=ram_array)
        if not rms.exists():
            messages.error(request, 'La memoria ram no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        prcsr = Processor.objects.get(id=processor)
        if prcsr is None:
            messages.error(request, 'El procesador no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        grphc = GraphicCard.objects.get(id=graphic)
        if grphc is None:
            messages.error(request, 'La tarjeta grafica no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        strg_array = storage.split(",")

        strg = Storage.objects.all().filter(id__in=strg_array)
        if not strg.exists():
            messages.error(request, 'El almacenamiento no existe')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        if image is None and product.image is None:
            messages.error(request, 'La imagen es requerida')
            return render(request, 'auth_user/admin/products/addproduct.html')
        
        if image is None:
            image = product.image
        
        product.name = name
        product.price = price
        product.stock = stock
        product.description = description
        product.brand = brnd
        product.processor = prcsr
        product.graphicscard = grphc
        product.image = image
        product.ram.set(rms)
        product.storage.set(strg)
        product.save()

        messages.success(request, f'Producto {product.name} actualizado correctamente')
        return redirect('dash-list-products')

    context = { "product": product, "brands": brands, "screens": screens, "processors": processors, "graphics": graphics, "rams": rams, "storages": storages}
    return render(request, 'auth_user/admin/products/edit.html', context)

@login_required
@permission_required('auth_user.view_user')
def removeproduct(request, id):
    product = Product.objects.get(id=id)
    if product is None:
        messages.error(request, 'El producto no existe')
        return redirect('dash-list-products')
    
    product.delete()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect('dash-list-products')

@login_required
@permission_required('auth_user.view_user')
def addcomponent(request, type):
    match (type):
        case "ram":
            rams = Ram.objects.all()
            if request.method == 'POST':
                name = request.POST.get('name')
                if Ram.objects.filter(name=name).exists():
                    messages.error(request, 'La memoria ram ya se encuentra registrada')
                    return render(request, 'auth_user/admin/products/components/addRam.html')
                
                ram = Ram.objects.create(name=name)
                ram.save()
                messages.success(request, 'Memoria ram registrada correctamente')
                return redirect('dash-ram')
            return render(request, 'auth_user/admin/products/components/addRam.html', {'rams': rams})
        case "graphics":
            graphics = GraphicCard.objects.all()
            if request.method == 'POST':
                name = request.POST.get('name')
                vram = request.POST.get('vram')
                fanquantity = request.POST.get('fanquantity')
                if GraphicCard.objects.filter(name=name).exists():
                    messages.error(request, 'La tarjeta grafica ya se encuentra registrada')
                    return render(request, 'auth_user/admin/products/components/addGraphics.html')
                
                graphics = GraphicCard.objects.create(name=name, vram=vram, fanquantity=fanquantity)
                graphics.save()
                messages.success(request, 'Tarjeta grafica registrada correctamente')
                return redirect('dash-graphics')
            return render(request, 'auth_user/admin/products/components/addGraphics.html', {'graphics': graphics})

        case "processor":
            processor = Processor.objects.all()
            if request.method == 'POST':
                name = request.POST.get('name')
                speed = request.POST.get('speed')
                coreq = request.POST.get('coreq')
                if Processor.objects.filter(name=name).exists():
                    messages.error(request, 'El procesador ya se encuentra registrado')
                    return render(request, 'auth_user/admin/products/components/addGraphics.html')
                
                processor = Processor.objects.create(name=name,speed=speed, coreq=coreq)
                processor.save()
                messages.success(request, 'Procesador registrado correctamente')
                return redirect('dash-processor')
            return render(request, 'auth_user/admin/products/components/addProcessor.html', {'processor': processor})    
        case "screen":
            techs = Screen._meta.get_field('technology').choices

            tech = []
            for t in techs:
                tech.append(t[0])

            if request.method == 'POST':
                name = request.POST.get('name')
                inches = request.POST.get('inches')
                refreshrate = request.POST.get('refreshrate')
                technology = request.POST.get('technology')
                
                if Screen.objects.filter(name=name).exists():
                    messages.error(request, 'La pantalla ya se encuentra registrada')
                    return render(request, 'auth_user/admin/products/components/addScreen.html')
                
                screen = Screen.objects.create(name=name, inches=inches, refreshrate=refreshrate, technology=technology)
                screen.save()
                messages.success(request, 'Pantalla registrada correctamente')
                return redirect('dash-screen')
            return render(request, 'auth_user/admin/products/components/addScreen.html', {'screen': tech})

        case "storage":
            storage = Storage._meta.get_field('technology').choices

            tech = []
            for t in storage:
                tech.append(t[0])

            if request.method == 'POST':
                name = request.POST.get('name')
                capacity = request.POST.get('capacity')
                technology = request.POST.get('technology')
                if Storage.objects.filter(name=name).exists():
                    messages.error(request, 'El almacenamiento ya se encuentra registrado')
                    return render(request, 'auth_user/admin/products/components/addStorage.html')
                
                storage = Storage.objects.create(name=name, capacity=capacity, technology=technology)
                storage.save()
                messages.success(request, 'Almacenamiento registrado correctamente')
                return redirect('dash-storage')
            return render(request, 'auth_user/admin/products/components/addStorage.html', {'storage': tech})
        case _:
            messages.error(request, 'Tipo de componente no valido')
            return redirect('dash-components')