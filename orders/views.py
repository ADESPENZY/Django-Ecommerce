from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from .forms import OrderCreateForm
from .models import Orderitem, Order

# Create your views here.
def order_create(request):
    cart = None
    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)  # Corrected `objects.get`

        if not cart or not cart.items.exists():  # Check if cart exists or is empty
            return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)  # Fixed POST method
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            for item in cart.items.all():
                Orderitem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

            # Delete the cart after order items have been created
            cart.delete()
            del request.session['cart_id']  # Fixed session key
            return redirect('orders:order_confirmation', order.id)
    else:
        form = OrderCreateForm()

    context = {
        "cart": cart,
        "form": form
    }

    return render(request, 'orders/order_create.html', context)

# Order confirmation view
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Corrected the object lookup
    return render(request, 'orders/order_confirmation.html', {'order': order})
