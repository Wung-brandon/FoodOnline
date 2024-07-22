from django.shortcuts import render, redirect
from django.http import HttpResponse
from marketplace.models import Cart
from marketplace.context_processor import get_cart_amounts
from .forms import OrderForm
import simplejson as json
from .models import Order, Payment, OrderFood
from .utils import generate_order_number
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    print(subtotal, total_tax, grand_total, tax_data)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save()  # order id/pk is generated
            order.order_number = generate_order_number(order.id)
            order.save()
            return redirect('place_order')
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')

def order_confirmed(request):
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']

@login_required(login_url='login')
def payments(request):
    # check if the request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':

        # store the payment in the payment model
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        print(order_number, transaction_id, payment_method, status)
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()

        # update the order model
        order.payment = payment
        order.is_ordered = True
        order.save()
        return HttpResponse('saved!')

        # check the payment details in the payment model
        # move the cart items to ordered food model
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity # total amount
            ordered_food.save()

        # send order confirmation email to the customer
        mail_subject = 'Thank you for ordering from foodonline shop!'
        mail_template = 'orders/order_confirmation.html'
        order_food = OrderFood()
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
            'order_food': order_food
        }
        send_notification(mail_subject, mail_template, context)
        return HttpResponse('Email sent!')



    # send order received email to the vendor

    # clear the cart if the payment is success

    # return back to ajax with the status or failure


