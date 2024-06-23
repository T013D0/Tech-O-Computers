from django.shortcuts import render, redirect
from .models import Product, Notebook, Computer, AllInOne, Brand, Recipe, RecipeDetails, Payment, Delivery
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib import messages
import datetime as dt
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
import random
import datetime
from django.core.mail import send_mail
from django.conf import settings
import pytz
from django.db.models import Q

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
        products = products.filter(Q(name__icontains=name) | Q(description__icontains=name) | Q(brand__name__icontains=name))
    
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

@require_POST
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    product = Product.objects.get(id=productId)
    recipe, created = Recipe.objects.get_or_create(client=request.user, complete=False)

    recipeDetails, created = RecipeDetails.objects.get_or_create(recipe=recipe, product=product)

    if action == 'add':
        if recipeDetails.quantity < product.stock:
            recipeDetails.quantity = (recipeDetails.quantity + 1)
    elif action == 'remove':
        recipeDetails.quantity = (recipeDetails.quantity - 1)
    elif action == 'delete':
        recipeDetails.quantity = 0

    recipeDetails.save()

    if recipeDetails.quantity <= 0:
        recipeDetails.delete()
    

    return JsonResponse('Item was added', safe=False)

@login_required
def cart(request):
    data = cart_data(request)
    items = data['items']
    recipe = data['recipe']

    context = { "items": items, "recipe": recipe}
    return render(request, 'store/cart.html', context)

@login_required
def shipping(request):
    data = cart_data(request)
    items = data['items']
    recipe = data['recipe']

    if items.count() == 0:
        messages.error(request, 'No hay productos en el carrito')
        return redirect('store')

    context = { "items": items, "recipe": recipe}
    return render(request, 'store/shipping.html', context)

@require_POST
def deliveryPost(request):
    if request.method == "POST":
        data = cart_data(request)
        recipe = data['recipe']
        request_data = json.loads(request.body)
        address = request_data.get('address')
        city = request_data.get('city')
        state = request_data.get('state')
        zip_code = request_data.get('postal_code')
        comments = request_data.get('comments')
        payment, createdP = Payment.objects.get_or_create(recipe=recipe)

        # Check if a Delivery object with the same recipe_id already exists
        delivery, created = Delivery.objects.get_or_create(
            recipe=recipe,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            comments=comments
        )

        # If the Delivery object was created, send a success response
        if created:
            return JsonResponse({'success': True})
        else:
            # If the Delivery object already existed, update it with the new data
            delivery.address = address
            delivery.city = city
            delivery.state = state
            delivery.zip_code = zip_code
            delivery.comments = comments
            delivery.save()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@ensure_csrf_cookie
@csrf_exempt
def webpay_plus_create(request):
    data = json.loads(request.body)
    amount = data.get('amount')
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    return_url = request.build_absolute_uri(location='commitpay/')

    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY))
    response = tx.create(buy_order, session_id, amount, return_url)
    return JsonResponse({'url': response['url'], 'token': response['token']}) 

@login_required

@csrf_exempt 
def commit_pay(request):
    token = request.GET.get('token_ws')
    TBK_TOKEN = request.POST.get('TBK_TOKEN')
    TBK_ID_SESSION = request.POST.get('TBK_ID_SESSION')
    TBK_ORDEN_COMPRA = request.POST.get('TBK_ORDEN_COMPRA')
    
    data = cart_data(request)
    recipe = data['recipe']
    payment = Payment.objects.get(recipe=recipe)
    
    #TRANSACCIÓN REALIZADA
    if TBK_TOKEN is None and TBK_ID_SESSION is None  and TBK_ORDEN_COMPRA is None and token is not None:
        #APROBAR TRANSACCION
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY))
        response = tx.commit(token)
        status = response.get('status')
        buy_order = response.get('buy_order')
        session_id = response.get('session_id')


        response_code = response.get('response_code')
        #TRANSACCIÓN APROBADA
        if status == 'AUTHORIZED' and response_code == 0:
            state = ''
            if response.get('status') == 'AUTHORIZED':
                state = 'Aceptado'
            pay_type = ''
            if response.get('payment_type_code') == 'VD':
                pay_type = 'Tarjeta de Débito'
            amount = int(response.get('amount'))
            amount = f'{amount:,.0f}'.replace(',', '.')
            transaction_date = dt.datetime.strptime(response.get('transaction_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
            transaction_date = '{:%d-%m-%Y %H%M:%S}'.format(transaction_date)
            transaction_detail = {
                'card_number': response.get('card_detail').get('card_number'),
                'transaction_date': transaction_date,
                'state': state,
                'pay_type': pay_type,
                'amount': amount,
                'authorization_code': response.get('authorization_code'),
                'buy_order': response.get('buy_order')
            }

            data = cart_data(request)
            recipe = data['recipe']
            recipe.complete = True
            recipe.transaction_id = response.get('buy_order')
            recipe.save()

            for item in data['items']:
                item.product.stock -= item.quantity
                item.product.save()

            print(response.get('payment_type_code'))

            if response.get('payment_type_code') == 'VD':
                payment.type = 'D'
            elif response.get('payment_type_code') == 'VN':
                payment.type = 'C'
            elif response.get('payment_type_code') == 'NC':
                payment.type = 'C'
            else:
                payment.type = 'T'

            payment.date_paid = datetime.datetime.now(tz=pytz.timezone('America/Santiago'))
            payment.paid = (response.get('status') == 'AUTHORIZED')
            payment.authorization_code = response.get('authorization_code')
            recipe.created_at = datetime.datetime.now(tz=pytz.timezone('America/Santiago'))

            if response.get('status') == 'AUTHORIZED':
                payment.status = 'A'

                #send email
                subject = 'Nueva Compra'
                message = 'Gracias por su compra, su transacción ha sido aprobada.'
                email_template_name = 'store/emails/payment_confirmation.html'
                to_email = request.user.email
                from_email = settings.EMAIL_HOST_USER

                send_mail(subject, message, html_message=render(request, email_template_name, {'recipe': recipe, 'items': data['items']}).content.decode('utf-8'), recipient_list=[to_email], from_email=from_email, fail_silently=False)

            else:
                payment.status = 'R'
            payment.save()
            recipe.save()

            return render(request, 'store/commitpay.html', {'transaction_detail': transaction_detail})
        else:
            payment.status = 'R'
            payment.save() # replace with your condition
            return render(request, 'store/refusedpay.html', {'transaction_detail': None})
    else:                             
        payment.status = 'R'
        payment.save()
        return render(request, 'store/refusedpay.html', {'transaction_detail': None})