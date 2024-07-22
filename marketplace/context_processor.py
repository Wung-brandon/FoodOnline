from .models import Cart
from menu.models import FoodItem
from marketplace.models import Tax



def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            # if the is cart item
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0

    return {'cart_count': cart_count}


def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        # looping through the all the food items in the cart
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (fooditem.price * item.quantity)

        # getting the tax from the database
        get_tax = Tax.objects.filter(is_active=True)
        # print(get_tax)
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((subtotal * tax_percentage) / 100, 2)
            print(tax_type, tax_percentage, tax_amount)
            tax_dict.update({tax_type: {str(tax_percentage): tax_amount}})

        # looping through the dictionary of the tax
        # for key in tax_dict.values():
        #     for x in key.values():
        #         tax = tax + x
        # print(tax)
        # print(tax_dict)

        # another way of solving this
        tax = sum(x for key in tax_dict.values() for x in key.values())
        print('tax--->', tax)
        print(tax_dict)
        grand_total = subtotal + tax
        return {
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,
            'tax_dict': tax_dict,

        }

    return {'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,

            }