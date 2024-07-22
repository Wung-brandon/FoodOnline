from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from django.contrib.auth.decorators import login_required
from .context_processor import get_cart_counter, get_cart_amounts
from orders.forms import OrderForm
from accounts.models import UserProfile


# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        # query to get hold of the food items of a particular category
        Prefetch(
            'food_items',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user has already addded the food item to the card
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase cart quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Increased cart quantity!',
                        'count_counter': get_cart_counter(request),
                        'qty': check_cart.quantity,
                        'cart_amount': get_cart_amounts(request)
                    })
                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Added the food to the cart!',
                        'count_counter': get_cart_counter(request),
                        'qty': check_cart.quantity,
                        'cart_amount': get_cart_amounts(request),
                    })

            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'This food item does not exists!'
                })

        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request!'
            })
    else:
        return JsonResponse({
            'status': 'login_required',
            'message': 'Please login to continue!'
        })



def decrease_cart(request, food_id=None):
    global check_cart
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user has already addded the food item to the card
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if check_cart.quantity > 1:
                        # decrease cart quantity
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Decrease cart quantity!',
                        'count_counter': get_cart_counter(request),
                        'qty': check_cart.quantity,
                        'cart_amount': get_cart_amounts(request),
                    })
                except:
                    return JsonResponse({
                        'status': 'Failed',
                        'message': 'You do not have any item in your cart!',
                        'count_counter': get_cart_counter(request),
                        'qty': check_cart.quantity,
                        'cart_amount': get_cart_amounts(request),
                    })

            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'This food item does not exists!'
                })

        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request!'
            })
    else:
        return JsonResponse({
            'status': 'login_required',
            'message': 'Please login to continue!'
        })


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                # check if cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Cart item has been deleted successfully!',
                        'count_counter': get_cart_counter(request),
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'Cart item does not exists!'
                })

        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request!'
            })

def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    r_name = request.GET['rest_name']
    print(address, longitude, latitude, radius, r_name)
    return render(request, 'marketplace/listings.html')

@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')

    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city' : user_profile.city,
        'pin_code' : user_profile.pin_code,

    }
    forms = OrderForm(initial=default_values)
    context = {
        'form': forms,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html', context)



