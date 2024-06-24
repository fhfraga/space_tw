import json

from .models import *


def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:	
			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
				cartItems += cart[i]['quantity']

				product = Product.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
				'digital':product.digital,'get_total':total,
				}
				items.append(item)

				if product.digital == False:
					order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

	
def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
		)
	return customer, order

def is_valid_card_number(card_number):
    """
    Verifica se o número do cartão de crédito é válido usando o algoritmo de Luhn.
    """
    card_number = card_number.replace(' ', '')  # Remover espaços em branco, se houver
    
    if not card_number.isdigit():
        return False
    
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    
    for count in range(0, num_digits):
        digit = int(card_number[count])
        
        if not ((count & 1) ^ oddeven):
            digit *= 2
        if digit > 9:
            digit -= 9
        
        sum += digit
    
    return (sum % 10) == 0


def is_valid_cvv(cvv):
    """
    Verifica se o CVV é válido.
    """
    if len(cvv) == 3 and cvv.isdigit():
        return True
    elif len(cvv) == 4 and cvv.isdigit():  
        return True
    else:
        return False