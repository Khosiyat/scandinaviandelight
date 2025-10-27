from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .decorators import *
from django.db.models import Sum



class MenuListView(ListView):
    model = Item
    template_name = 'main/home.html'
    context_object_name = 'menu_items'

def menuDetail(request, slug):
    item = Item.objects.filter(slug=slug).first()
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7] 
    context = {
        'item' : item,
        'reviews' : reviews,
    }
    return render(request, 'main/dishes.html', context)

@login_required
def add_reviews(request):
    if request.method == "POST":
        user = request.user
        rslug = request.POST.get("rslug")
        item = Item.objects.get(slug=rslug)
        review = request.POST.get("review")

        reviews = Reviews(user=user, item=item, review=review, rslug=rslug)
        reviews.save()
        messages.success(request, "Thankyou for reviewing this product!!")
    return redirect(f"/dishes/{item.slug}")

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/item_list'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False



  
class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.user:
            return True
        return False


# ------------------ admin
@login_required(login_url='/accounts/login/')
@admin_required
def admin_view(request):
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Delivered").order_by('-ordered_date')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'main/admin_view.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def item_list(request):
    items = Item.objects.filter(created_by=request.user)
    context = {
        'items':items
    }
    return render(request, 'main/item_list.html', context)

@login_required
@admin_required
def update_status(request,pk):
    if request.method == 'POST':
        status = request.POST['status']
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Active",pk=pk)
    delivery_date=timezone.now()
    if status == 'Delivered':
        cart_items.update(status=status, delivery_date=delivery_date)
    return render(request, 'main/pending_orders.html')


@login_required(login_url='/accounts/login/')
@admin_required
def admin_dashboard(request):
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True)
    pending_total = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Active").count()
    completed_total = CartItems.objects.filter(item__created_by=request.user, ordered=True,status="Delivered").count()
    count1 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="3").count()
    count2 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="4").count()
    count3 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="5").count()
    total = CartItems.objects.filter(item__created_by=request.user, ordered=True).aggregate(Sum('item__price'))
    income = total.get("item__price__sum")
    context = {
        'pending_total' : pending_total,
        'completed_total' : completed_total,
        'income' : income,
        'count1' : count1,
        'count2' : count2,
        'count3' : count3,
    }
    return render(request, 'main/admin_dashboard.html', context)


# ----------------------------------------------
# Homepage: List of ingredients
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'main/home.html', {'ingredients': ingredients})
 
 

# Checkout (place order)
@login_required
def order_item(request):
    cart_items = CartItems.objects.filter(user=request.user, ordered=False)
    ordered_date = timezone.now()
    cart_items.update(ordered=True, ordered_date=ordered_date)
    messages.info(request, "Order placed successfully!")
    return redirect("main:order_details")


# ----------------------------------------------

# Admin: Pending orders
@login_required
def pending_orders(request):
    orders = Order.objects.filter(status="Active").order_by('-ordered_date')
    return render(request, 'main/pending_orders.html', {'orders': orders})


# Admin: Update status
@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.status = request.POST.get("status", "Active")
        order.save()
        messages.success(request, f"Order {order.reference_code} marked as {order.status}")
    return redirect("main:pending_orders")



# ----------------------------------


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Ingredient, Snack, CartItems, Order

 
def home(request):
    ingredients = Ingredient.objects.all().order_by('price_per_100g')  # ascending by ingredient price
    snacks = Snack.objects.all().order_by('price')  # ascending by snack price
    return render(request, 'main/home.html', {'ingredients': ingredients, 'snacks': snacks})

# ---------------- Ingredient Detail ----------------
def ingredient_detail(request, slug):
    ingredient = get_object_or_404(Ingredient, slug=slug)
    return render(request, 'main/ingredient_detail.html', {'ingredient': ingredient})

# ---------------- Add Ingredients to Cart ----------------
@login_required
def add_to_cart(request, slug):
    ingredient = get_object_or_404(Ingredient, slug=slug)
    grams = int(request.POST.get("grams", 100))
    CartItems.objects.create(
        ingredient=ingredient,
        user=request.user,
        grams=grams,
        ordered=False,
    )
    messages.success(request, f"Added {grams}g of {ingredient.title} to cart!")
    return redirect("main:cart")

# ---------------- Add Snack to Cart ----------------
@login_required
def add_snack_to_cart(request, pk):
    snack = get_object_or_404(Snack, pk=pk)
    quantity = int(request.POST.get("quantity", 1))
    CartItems.objects.create(
        snack=snack,
        user=request.user,
        quantity=quantity,
        ordered=False
    )
    messages.success(request, f"Added {quantity} pcs of {snack.title} to cart!")
    return redirect("main:cart")


@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user, ordered=False)
    total_cost = sum(item.get_total_price() for item in cart_items)

    # --- Check for nuts-only snack ---
    nut_ingredients = [item for item in cart_items if item.ingredient and item.ingredient.category == 'nut']
    sweet_ingredients = [item for item in cart_items if item.ingredient and item.ingredient.category == 'sweet']
    nuts_only_warning = False
    if nut_ingredients and not sweet_ingredients:
        nuts_only_warning = True

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'nuts_only_warning': nuts_only_warning
    }
    return render(request, 'main/cart.html', context)

# ---------------- Remove from Cart ----------------
@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItems, pk=pk, user=request.user, ordered=False)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("main:cart")
 
 
# views.py (checkout)
@login_required
def checkout(request):
    ingredients = CartItems.objects.filter(user=request.user, ordered=False, ingredient__isnull=False)
    snacks = CartItems.objects.filter(user=request.user, ordered=False, snack__isnull=False)

    # Check custom snack rules
    nut_ingredients = [item for item in ingredients if item.ingredient.category == 'nut']
    sweet_ingredients = [item for item in ingredients if item.ingredient.category == 'sweet']

    if nut_ingredients and not sweet_ingredients:
        messages.error(request, "A snack cannot be made with only nuts. Add at least one sweet ingredient (like honey, raisins, or apricot).")
        return redirect("main:cart")  # redirect back to cart

    # Proceed as normal
    total_ingredient_grams = sum(item.grams for item in ingredients)
    total_ingredient_price = sum(item.get_total_price() for item in ingredients)
    total_snacks_price = sum(item.get_total_price() for item in snacks)
    total_cost = total_ingredient_price + total_snacks_price

    if request.method == "POST":
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())

        if ingredients.exists():
            CartItems.objects.create(
                user=request.user,
                ingredient=None,
                snack=None,
                grams=total_ingredient_grams,
                ordered=True,
                order=order
            )
            ingredients.update(ordered=True, order=order)

        for snack_item in snacks:
            snack_item.ordered = True
            snack_item.order = order
            snack_item.save()

        messages.success(request, f"Order {order.reference_code} placed successfully!")
        return redirect("main:order_details")

    context = {
        "ingredients_grouped": ingredients,
        "snacks": snacks,
        "total_ingredient_grams": total_ingredient_grams,
        "total_ingredient_price": total_ingredient_price,
        "total_cost": total_cost
    }
    return render(request, "main/checkout.html", context)


# ---------------- Order Details ----------------
@login_required
def order_details(request):
    active_orders = Order.objects.filter(user=request.user, status="Active").order_by('-ordered_date')
    past_orders = Order.objects.filter(user=request.user, status="Delivered").order_by('-ordered_date')

    return render(request, "main/order_details.html", {
        "active_orders": active_orders,
        "past_orders": past_orders,
    })


def snacks_list(request):
    snacks = Snack.objects.all().order_by('price')  # ascending order
    return render(request, "main/snacks_list.html", {"snacks": snacks})
 


 
def order_success(request):
    return render(request, "main/order_success.html")


