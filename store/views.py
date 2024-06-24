import datetime
import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .utils import (cartData, cookieCart, guestOrder, is_valid_card_number,
                    is_valid_cvv)


def store(request):
    products = Product.objects.filter(on_sale=True)
    return render(request, 'store/store.html', {'products': products})

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


def about(request):
    return render(request, 'store/about.html') 

def sala_aracatiba(request):
    return render(request, 'store/rooms/sala_1.html')  

def sala_centro(request):
    return render(request, 'store/rooms/sala_2.html')  

def sala_itapeba(request):
    return render(request, 'store/rooms/sala_3.html')  

def auditorio_inoa(request):
    return render(request, 'store/rooms/auditorio_1.html')  

def finish(request):
    return render(request, 'store/finish.html')  

def shared_space(request):
    shared_space_products = Product.objects.filter(space_type='compartilhado')
    return render(request, 'store/shared_space.html', {'shared_space_products': shared_space_products})

def office_spaces(request):
    office_products = Product.objects.filter(space_type='escritorio')
    return render(request, 'store/office_spaces.html', {'office_products': office_products})

def auditorium_spaces(request):
    auditorium_products = Product.objects.filter(space_type='auditorio')
    return render(request, 'store/auditorium_spaces.html', {'auditorium_products': auditorium_products})

def search_results(request):
    query = request.GET.get('query')

    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = Product.objects.none()

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'store/search.html', context)

def validar_transacao(request):
    if request.method == 'POST':
        data = request.POST
        card_number = data.get('card-number')
        cvv = data.get('cvv')
        
        if is_valid_card_number(card_number) and is_valid_cvv(cvv):
            finish_url = reverse('finish')
            return JsonResponse({'success': True, 'redirect_url': finish_url})
        else:
            return JsonResponse({'success': False, 'error': 'Número do cartão inválido.'})
    return JsonResponse({'success': False, 'error': 'Método não permitido.'})

def privacy_policy(request):
    return render(request, 'store/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'store/terms_of_service.html')