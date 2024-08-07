from django.shortcuts import render, redirect
from django.contrib import messages
from auth_user.models import User
from store.models import Product, Brand, Ram, Storage, Processor, GraphicCard, Screen
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from store.models import Product, Notebook, Computer, AllInOne, Brand, Recipe, RecipeDetails, Delivery, Payment
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Sum, F, IntegerField
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from .tokens import account_activation_token
from django.http import JsonResponse
from django.core.serializers import serialize
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from .forms import RegisterForm, LoginForm
import json
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Tu cuenta fue verificada ya puedes iniciar sesion')
        return redirect('login')
    else:
        messages.error(request, 'Link de activacion invalido!')
    return redirect('index')

def emailActivation(request, user, to_email):
    #send email
    subject = 'Completa tu registro'
    message = 'Confirma tu registro para acceder a tu cuenta'
    email_template_name = 'auth_user/emails/registration.html'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, html_message=render(request, email_template_name, {'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user), 'domain': get_current_site(request).domain, 'user': user.get_full_name, 'protocol': 'https' if request.is_secure() else 'http'}).content.decode('utf-8'), recipient_list=[to_email], from_email=from_email, fail_silently=False)
    messages.success(request, 'Se envio un correo para que confirmes tu cuenta, recuerda verificar tu carpeta de spam')

# Create your views here.
def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Bienvenido ' + user.get_full_name() +  '!')

                next = request.GET.get('next')
                if next is not None and next != '':
                    return redirect(next)
                else:
                    return redirect('index')
            else:
                messages.error(request, 'Email o Contraseña incorrectos')
                return redirect('login')
        else:
            messages.error(request, 'Email o Contraseña incorrectos')
            return redirect('login')
    return render(request, 'auth_user/login.html')

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            emailActivation(request, user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            if form.errors.get('rut') is not None:
                messages.error(request, 'El rut ya se encuentra registrado')
            elif form.errors.get('email') is not None:
                messages.error(request, 'El email ya se encuentra registrado')
            elif form.errors.get('password1') is not None:
                messages.error(request, 'Las contraseñas no coinciden')
            elif form.errors.get('password2') is not None:
                messages.error(request, 'La contraseña es demasiado comun')
            elif form.errors.get('first_name') is not None:
                messages.error(request, 'El nombre es requerido')
            elif form.errors.get('last_name') is not None:
                messages.error(request, 'El apellido es requerido')
            else:
                messages.error(request, 'Error al registrar el usuario')
            return redirect('register')
        
    context = {'form': RegisterForm()}
    return render(request, 'auth_user/register.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def dashboard(request):
    count_products = Product.objects.all().count()
    count_sell = Recipe.objects.filter(complete=True).all().count()
    profit = RecipeDetails.objects.all().aggregate(profit=Sum(F('product__price') * F('quantity'), output_field=IntegerField()))['profit']
    data = []
    for i in range(1, 13):
        data.append(Recipe.objects.filter(created_at__month=i,complete=True).count())

    products = Product.objects.all()
    context = { "count_products": count_products, "count_sell": count_sell, "profit": profit, "data": data, "products": products}
    return render(request, 'auth_user/admin/dashboard.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def packages(request):
    return render(request, 'auth_user/admin/packages.html')

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def transactions(request):
    return render(request, 'auth_user/admin/transactions.html')

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def brands(request):
    brands = Brand.objects.all()
    context = {'brands' : brands}
    return render(request, 'auth_user/admin/products/brands.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def graphics(request):
    graphics = GraphicCard.objects.all()
    context = {'graphics' : graphics}
    return render(request, 'auth_user/admin/products/graphics.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def processor(request):
    processor = Processor.objects.all()
    context = {'processor' : processor}
    return render(request, 'auth_user/admin/products/processor.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def ram(request):
    ram = Ram.objects.all()
    context = {'ram' : ram}
    return render(request, 'auth_user/admin/products/ram.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def screen(request):
    screen = Screen.objects.all()
    context = {'screen' : screen}
    return render(request, 'auth_user/admin/products/screen.html', context)


@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def storage(request):
    storage = Storage.objects.all()
    context = {'storage' : storage}
    return render(request, 'auth_user/admin/products/storage.html', context)


@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def components(request):
    return render(request, 'auth_user/admin/products/components.html')

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
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

        if int(price) < 0:
            messages.error(request, 'El precio debe ser mayor a 0')
            return redirect('dash-addproduct')
        
        if int(stock) < 0:
            messages.error(request, 'El stock debe ser mayor a 0')
            return redirect('dash-addproduct')

        if Product.objects.filter(name=name).exists():
            messages.error(request, 'El producto ya se encuentra registrado')
            return redirect('dash-addproduct')
        
        brnd = Brand.objects.get(id=brand)
        if brnd is None:
            messages.error(request, 'La marca no existe')
            return redirect('dash-addproduct')
        
        if type == "notebook" or type == "all-in-one":
            scrn = Screen.objects.get(id=screen)
            if scrn is None:
                messages.error(request, 'La pantalla no existe')
                return redirect('dash-addproduct')

        ram_array = ram.split(",")

        rms = Ram.objects.all().filter(id__in=ram_array)
        if not rms.exists():
            messages.error(request, 'La memoria ram no existe')
            return redirect('dash-addproduct')
        
        prcsr = Processor.objects.get(id=processor)
        if prcsr is None:
            messages.error(request, 'El procesador no existe')
            return redirect('dash-addproduct')
        
        grphc = GraphicCard.objects.get(id=graphic)
        if grphc is None:
            messages.error(request, 'La tarjeta grafica no existe')
            return redirect('dash-addproduct')
        
        strg_array = storage.split(",")

        strg = Storage.objects.all().filter(id__in=strg_array)
        if not strg.exists():
            messages.error(request, 'El almacenamiento no existe')
            return redirect('dash-addproduct')
        
        if image.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'webp', 'svg']:
            messages.error(request, 'Formato de imagen no valido')
            return redirect('dash-addproduct')
        
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
@permission_required('auth_user.view_user', raise_exception=True)
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


    products = products.order_by("-created_at")
    
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    if page is None or page == "":
        page = 1

    context = { "products": paginator.get_page(page).object_list, "page_obj": paginator.get_page(page), "per_page": paginator.per_page, "total_range": paginator.page_range, "total": products.count(), "brands": brands}
    return render(request, 'auth_user/admin/products/list.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def users(request):
    user = User.objects.all()

    context = {'usuarios' : user}
    return render(request, 'auth_user/admin/users.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def removeuser(request, id):

    user = User.objects.get(rut=id)
    if user is None:
        messages.error(request, 'El usuario no existe')
        return redirect('dash-users')
    
    if user == request.user:
        messages.error(request, 'No puedes eliminarte a ti mismo')
        return redirect('dash-users')
    
    if user.is_superuser:
        messages.error(request, 'No puedes eliminar un usuario administrador')
        return redirect('dash-users')
    
    if user.is_staff:
        messages.error(request, 'No puedes eliminar un usuario staff')
        return redirect('dash-users')
    
    
    user.delete()
    messages.success(request, 'Usuario eliminado correctamente')
    return redirect('dash-users')


@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def removeOrder(request, id):
    order = Recipe.objects.get(id=id)
    if order is None:
        messages.error(request, 'La orden no existe')
        return redirect('dash-orders')
    
    order.delete()
    messages.success(request, 'Orden eliminada correctamente')
    return redirect('dash-orders')

@login_required
@permission_required('auth_user.change_user', raise_exception=True)
def edituser(request, id):
        user = User.objects.get(rut=id)

        if user is None:
            messages.error(request, 'Usuario no encontrado')
            return redirect('dash-users')

        if request.method == 'POST':

            if user == request.user:
                messages.error(request, 'No puedes editar tu propio usuario')
                return redirect('dash-users')
            
            if user.is_superuser:
                messages.error(request, 'No puedes editar un usuario administrador')
                return redirect('dash-users')
            
            if user.is_staff:
                messages.error(request, 'No puedes editar un usuario staff')
                return redirect('dash-users')
            
            rut = request.POST.get('rut')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            admin = request.POST.get('admin') == 'on'
            staff = request.POST.get('staff') == 'on'
            active = request.POST.get('active') == 'on'
            
            user.rut = rut
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_superuser = admin
            user.is_staff = staff
            user.is_active = active
            user.save()
            messages.success(request, 'Usuario actualizado correctamente')
            return redirect('dash-users')

        context = {'user': user}
        return render(request, 'auth_user/admin/editusers.html', context)


@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def userorders(request, id):
    user = User.objects.get(rut=id)
    orders = Recipe.objects.filter(complete=True, client=user ).all()

    orderByDate = request.GET.get('orderByDate')
    if orderByDate is not None:
        if orderByDate == 'asc':
            orders = orders.order_by('created_at')
        elif orderByDate == 'desc':
            orders = orders.order_by('-created_at')

    context = {'orders' : orders, 'user': user}
    return render(request, 'auth_user/admin/ordersusers.html', context)


@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def delivery(request):
    delivery = Delivery.objects.all()
    context = {'delivery' : delivery}
    return render(request, 'auth_user/admin/delivery.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def orders(request):
    orders = Recipe.objects.filter(complete=True).all()

    orderByDate = request.GET.get('orderByDate')
    if orderByDate is not None:
        if orderByDate == 'asc':
            orders = orders.order_by('created_at')
        elif orderByDate == 'desc':
            orders = orders.order_by('-created_at')
            
    context = {'orders' : orders}
    return render(request, 'auth_user/admin/orders.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def orderdetail(request, id):
    order = Recipe.objects.get(id=id)

    if order is None:
        messages.error(request, 'La orden no existe')
        return redirect('dash-orders')
    
    details = RecipeDetails.objects.filter(recipe=order).all()
    context = {'order' : order, 'details': details}
    return render(request, 'auth_user/admin/orderdetail.html', context)

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
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

        if int(stock) < 0:
            messages.error(request, 'El stock debe ser mayor a 0')
            return redirect('dash-editproduct', id=id)
    
        if int(price) < 0:
            messages.error(request, 'El precio debe ser mayor a 0')
            return redirect('dash-editproduct', id=id)

        if not Product.objects.filter(name=name).exists():
            messages.error(request, 'El producto no existe')
            return redirect('dash-list-products')
        
        brnd = Brand.objects.get(id=brand)
        if brnd is None:
            messages.error(request, 'La marca no existe')
            return redirect('dash-editproduct', id=id)
        
        if type == "notebook" or type == "all-in-one":
            scrn = Screen.objects.get(id=screen)
            if scrn is None:
                messages.error(request, 'La pantalla no existe')
                return redirect('dash-editproduct', id=id)

        ram_array = ram.split(",")

        rms = Ram.objects.all().filter(id__in=ram_array)
        if not rms.exists():
            messages.error(request, 'La memoria ram no existe')
            return redirect('dash-editproduct', id=id)
        
        prcsr = Processor.objects.get(id=processor)
        if prcsr is None:
            messages.error(request, 'El procesador no existe')
            return redirect('dash-editproduct', id=id)
        
        grphc = GraphicCard.objects.get(id=graphic)
        if grphc is None:
            messages.error(request, 'La tarjeta grafica no existe')
            return redirect('dash-editproduct', id=id)
        
        strg_array = storage.split(",")

        strg = Storage.objects.all().filter(id__in=strg_array)
        if not strg.exists():
            messages.error(request, 'El almacenamiento no existe')
            return redirect('dash-editproduct', id=id)
        
        if image is None and product.image is None:
            messages.error(request, 'La imagen es requerida')
            return redirect('dash-editproduct', id=id)
        
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
@permission_required('auth_user.view_user', raise_exception=True)
def addbrand(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        if Brand.objects.filter(name=name).exists():
            messages.error(request, 'La marca ya se encuentra registrada')
            return('addbrand')
        
        brand = Brand.objects.create(name=name)
        brand.save()
        messages.success(request, 'Marca registrada correctamente')
        return redirect('dash-brands')
    return render(request, 'auth_user/admin/products/components/addbrands.html')

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def removebrand(request, id):

    brand = Brand.objects.get(id=id)
    if brand is None:
        messages.error(request, 'La marca no existe')
        return redirect('dash-brands')
    
    brand.delete()
    messages.success(request, 'Marca eliminada correctamente')
    return redirect('dash-brands')

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def removeproduct(request, id):
    product = Product.objects.get(id=id)
    if product is None:
        messages.error(request, 'El producto no existe')
        return redirect('dash-list-products')
    
    product.delete()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect('dash-list-products')

@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def addcomponent(request, type):
    match (type):
        case "ram":
            rams = Ram.objects.all()
            if request.method == 'POST':
                name = request.POST.get('name')
                if Ram.objects.filter(name=name).exists():
                    messages.error(request, 'La memoria ram ya se encuentra registrada')
                    return redirect('dash-ram')
                
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
                    return redirect('dash-storage')
                
                storage = Storage.objects.create(name=name, capacity=capacity, technology=technology)
                storage.save()
                messages.success(request, 'Almacenamiento registrado correctamente')
                return redirect('dash-storage')
            return render(request, 'auth_user/admin/products/components/addStorage.html', {'storage': tech})
        case _:
            messages.error(request, 'Tipo de componente no valido')
            return redirect('dash-components')
        
@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def editComponent(request, type, id):
    match (type):
        case "ram":
            ram = Ram.objects.get(id=id)
            if request.method == 'POST':
                name = request.POST.get('name')
                if not Ram.objects.filter(id=ram.id).exists():
                    messages.error(request, 'La memoria ram no existe')
                    return redirect('dash-ram')
                ram.name = name
                ram.save()
                messages.success(request, 'Memoria ram actualizada correctamente')
                return redirect('dash-ram')
            return render(request, 'auth_user/admin/products/components/editRam.html', {'ram': ram})
        case "graphics":
            graphic = GraphicCard.objects.get(id=id)
            if request.method == 'POST':
                name = request.POST.get('name')
                vram = request.POST.get('vram')
                fanquantity = request.POST.get('fanquantity')
                if not GraphicCard.objects.filter(id=graphic.id).exists():
                    messages.error(request, 'La tarjeta grafica no existe')
                    return redirect('dash-graphics')
                
                graphic.name = name
                graphic.vram = vram
                graphic.fanquantity = fanquantity
                graphic.save()
                messages.success(request, 'Tarjeta grafica actualizada correctamente')
                return redirect('dash-graphics')
            return render(request, 'auth_user/admin/products/components/editGraphics.html', {'graphic': graphic})
        case "processor":
            processor = Processor.objects.get(id=id)
            if request.method == 'POST':
                name = request.POST.get('name')
                speed = request.POST.get('speed')
                coreq = request.POST.get('coreq')

                if not Processor.objects.filter(id=processor.id).exists():
                    messages.error(request, 'El procesador no existe')
                    return redirect('dash-processor')
                
                processor.name = name
                processor.speed = speed
                processor.coreq = coreq
                processor.save()
                messages.success(request, 'Procesador actualizado correctamente')
                return redirect('dash-processor')
            return render(request, 'auth_user/admin/products/components/editProcessor.html', {'processor': processor})
        case "screen":
            screen = Screen.objects.get(id=id)
            techs = Screen._meta.get_field('technology').choices

            tech = []
            for t in techs:
                tech.append(t[0])

            if request.method == 'POST':
                name = request.POST.get('name')
                inches = request.POST.get('inches')
                refreshrate = request.POST.get('refreshrate')
                technology = request.POST.get('technology')
                
                if not Screen.objects.filter(id=screen.id).exists():
                    messages.error(request, 'La pantalla no existe')
                    return redirect('dash-screen')
                
                screen.name = name
                screen.inches = inches
                screen.refreshrate = refreshrate
                screen.technology = technology
                screen.save()
                messages.success(request, 'Pantalla actualizada correctamente')
                return redirect('dash-screen')
            return render(request, 'auth_user/admin/products/components/editScreen.html', {'screen': screen, 'tech': tech})
        case "storage":

            storage = Storage.objects.get(id=id)
            storage_choices = Storage._meta.get_field('technology').choices

            tech = []

            for t in storage_choices:
                tech.append(t[0])

            if request.method == 'POST':
                name = request.POST.get('name')
                capacity = request.POST.get('capacity')
                technology = request.POST.get('technology')

                if not Storage.objects.filter(id=storage.id).exists():
                    messages.error(request, 'El almacenamiento no existe')
                    return redirect('dash-storage')
                
                storage.name = name
                storage.capacity = capacity
                storage.technology = technology
                storage.save()
                messages.success(request, 'Almacenamiento actualizado correctamente')
                return redirect('dash-storage')
            return render(request, 'auth_user/admin/products/components/editStorage.html', {'storage': storage, 'tech': tech})
        case _:
            messages.error(request, 'Tipo de componente no valido')
            return redirect('dash-components')
        
@require_POST
def editDeliveryStatus(request):
    data = json.loads(request.body)
    id = data['id']
    status = data['status']
    delivery = Delivery.objects.get(id=id)
    if delivery is None:
        return HttpResponse({'message': 'El despacho no existe'}, status=404)
    
    delivery.status = status
    delivery.save()
    return HttpResponse({'message': 'Despacho actualizado correctamente'}, status=200)
        
@login_required
@permission_required('auth_user.view_user', raise_exception=True)
def removeComponent(request, type, id):

    match (type):
        case "ram":
            ram = Ram.objects.get(id=id)
            if ram is None:
                messages.error(request, 'La memoria ram no existe')
                return redirect('dash-ram')
            
            ram.delete()
            messages.success(request, 'Memoria ram eliminada correctamente')
            return redirect('dash-ram')
        case "graphics":
            graphic = GraphicCard.objects.get(id=id)
            if graphic is None:
                messages.error(request, 'La tarjeta grafica no existe')
                return redirect('dash-graphics')
            
            graphic.delete()
            messages.success(request, 'Tarjeta grafica eliminada correctamente')
            return redirect('dash-graphics')
        case "processor":
            processor = Processor.objects.get(id=id)
            if processor is None:
                messages.error(request, 'El procesador no existe')
                return redirect('dash-processor')
            
            processor.delete()
            messages.success(request, 'Procesador eliminado correctamente')
            return redirect('dash-processor')
        case "screen":
            screen = Screen.objects.get(id=id)
            if screen is None:
                messages.error(request, 'La pantalla no existe')
                return redirect('dash-screen')
            
            screen.delete()
            messages.success(request, 'Pantalla eliminada correctamente')
            return redirect('dash-screen')
        case "storage":
            storage = Storage.objects.get(id=id)
            if storage is None:
                messages.error(request, 'El almacenamiento no existe')
                return redirect('dash-storage')
            
            storage.delete()
            messages.success(request, 'Almacenamiento eliminado correctamente')
            return redirect('dash-storage')
        case _:
            messages.error(request, 'Tipo de componente no valido')
            return redirect('dash-components')