from .models import Cart, FoodItem, Tax


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)




from decimal import Decimal, ROUND_HALF_UP

def get_cart_amounts(request):
    subtotal = Decimal('0.00')
    tax = Decimal('0.00')
    grand_total = Decimal('0.00')
    tax_dict = {}

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            try:
                food = FoodItem.objects.get(pk=item.food_item.id)
                if food.total_cost is not None and item.quantity is not None:
                    subtotal += food.total_cost * item.quantity
            except FoodItem.DoesNotExist:
                continue

       

        grand_total = subtotal 

    return {
        'subtotal': subtotal,
        'tax': tax,
        'grand_total': grand_total,
        'tax_dict': tax_dict
    }
