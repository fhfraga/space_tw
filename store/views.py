import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import ProductForm, UserRegisterForm
from .models import *
from .utils import cartData, cookieCart, guestOrder, is_valid_card_number, is_valid_cvv

today = timezone.now().date()  # Obtém a data atual


def store(request):
    products = Product.objects.filter(
        on_sale=True,
        is_rented=False,
        available_from__lte=today,
        available_to__gte=today,
    )
    return render(request, "store/store.html", {"products": products})

def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    print("Action:", action)
    print("Product:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # Verifique se o produto já está no carrinho
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        if orderItem.quantity > 0:
            return JsonResponse(
                {"status": "exists", "message": "Este produto já está no carrinho."},
                safe=False,
            )
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    return JsonResponse("Payment submitted..", safe=False)


def about(request):
    return render(request, "store/about.html")

def sala_aracatiba(request):
    return render(request, "store/rooms/sala_1.html")

def sala_centro(request):
    return render(request, "store/rooms/sala_2.html")

def sala_itapeba(request):
    return render(request, "store/rooms/sala_3.html")

def auditorio_inoa(request):
    return render(request, 'store/rooms/auditorio_1.html')  

def finish(request):
    return render(request, 'store/finish.html') 

def shared_space(request):
    shared_space_products = Product.objects.filter(
        space_type="compartilhado",
        is_rented=False,
        available_from__lte=today,
        available_to__gte=today,
    )
    return render(
        request,
        "store/shared_space.html",
        {"shared_space_products": shared_space_products},
    )


def office_spaces(request):
    office_products = Product.objects.filter(
        space_type="escritorio",
        is_rented=False,
        available_from__lte=today,
        available_to__gte=today,
    )
    return render(
        request, "store/office_spaces.html", {"office_products": office_products}
    )


def auditorium_spaces(request):
    auditorium_products = Product.objects.filter(
        space_type="auditorio",
        is_rented=False,
        available_from__lte=today,
        available_to__gte=today,
    )
    return render(
        request,
        "store/auditorium_spaces.html",
        {"auditorium_products": auditorium_products},
    )


def search_results(request):
    query = request.GET.get("query")

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query)
            | Q(features__icontains=query)
            | Q(space_type__icontains=query)
        )
    else:
        results = Product.objects.none()

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "store/search.html", context)


def validar_transacao(request):
    if request.method == "POST":
        data = request.POST
        card_number = data.get("card-number")
        cvv = data.get("cvv")

        # Obtenha o cliente autenticado
        if request.user.is_authenticated:
            customer = request.user.customer
            try:
                # Obtenha o pedido que está sendo finalizado
                order = Order.objects.get(customer=customer, complete=False)
            except Order.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Pedido não encontrado."}
                )

            if is_valid_card_number(card_number) and is_valid_cvv(cvv):
                # Marcar o pedido como completo
                order.complete = True
                order.save()

                # Atualize o status dos produtos no pedido
                for item in order.orderitem_set.all():
                    product = item.product
                    # product.on_sale = False
                    product.is_rented = True
                    product.save()

                # Redirecionar para a página de finalização
                finish_url = reverse("finish")
                return JsonResponse({"success": True, "redirect_url": finish_url})
            else:
                return JsonResponse(
                    {"success": False, "error": "Número do cartão ou CVV inválido."}
                )
        else:
            return JsonResponse({"success": False, "error": "Usuário não autenticado."})
    return JsonResponse({"success": False, "error": "Método não permitido."})


def privacy_policy(request):
    return render(request, "store/privacy_policy.html")


def terms_of_service(request):
    return render(request, "store/terms_of_service.html")


def store_index(request):
    if request.user.is_authenticated:
        return render(request, template_name="store.html")
    else:
        return redirect("store_login")


def store_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("store")
    return render(request, template_name="store/login.html")


def store_logout(request):
    logout(request)
    return redirect("store_login")


@login_required
def create_room(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect("store")
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "store/create_room.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Sua conta foi criada! Você já pode fazer login."
            )
            return redirect("store_login")
    else:
        form = UserRegisterForm()
    return render(request, "store/register.html", {"form": form})
