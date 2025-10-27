from django.contrib import admin
from .models import Ingredient, Snack, CartItems, Order

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_per_100g', 'created_by']

@admin.register(Snack)
class SnackAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "created_by", "created_at"]

class CartItemsInline(admin.TabularInline):
    model = CartItems
    extra = 0
    readonly_fields = ['ingredient', 'snack', 'grams', 'quantity', 'get_total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = "Price (SEK)"



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'reference_code',
        'user',
        'get_email',
        'status',
        'ordered_date',
        'get_total_cost'
    ]
    list_filter = ['status', 'ordered_date']
    inlines = [CartItemsInline]

    def get_total_cost(self, obj):
        return obj.get_total_cost()
    get_total_cost.short_description = "Total Cost (SEK)"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"
