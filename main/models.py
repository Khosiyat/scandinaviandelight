from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# ---------------- Item ----------------

class Item(models.Model):
    LABELS = (
        ('BestSeller', 'BestSeller'),
        ('New', 'New'),
        ('Spicy🔥', 'Spicy🔥'),
    )   

    LABEL_COLOUR = (
        ('danger', 'danger'),
        ('success', 'success'),
        ('primary', 'primary'),
        ('info', 'info')
    )
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250,blank=True)
    price = models.FloatField()
    pieces = models.IntegerField(default=6)
    instructions = models.CharField(max_length=250,default="Jain Option Available")
    image = models.ImageField(default='default.png', upload_to='images/')
    labels = models.CharField(max_length=25, choices=LABELS, blank=True)
    label_colour = models.CharField(max_length=15, choices=LABEL_COLOUR, blank=True)
    slug = models.SlugField(default="sushi_name")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:dishes", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_item_delete_url(self):
        return reverse("main:item-delete", kwargs={
            'slug': self.slug
        })

    def get_update_item_url(self):
        return reverse("main:item-update", kwargs={
            'slug': self.slug
        })

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    rslug = models.SlugField()
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review




from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
import uuid


# models.py
class Ingredient(models.Model):
    CATEGORY_CHOICES = (
        ('nut', 'Nut'),
        ('sweet', 'Sweet'),  # dried fruit or honey
        ('other', 'Other'),
    )

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250, blank=True)
    price_per_100g = models.FloatField(help_text="Price per 100 grams")
    image = models.ImageField(default='default.png', upload_to='images/')
    is_nut = models.BooleanField(default=False)
    is_sweet = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other')  # NEW FIELD

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:ingredient-detail", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={'slug': self.slug})



# ---------------- Snacks ----------------
class Snack(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="snacks/")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ---------------- Orders ----------------
class Order(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered'),
    )

    SUBSCRIPTION_CHOICES = (
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=100, unique=True, editable=False)
    ordered_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    subscription_type = models.CharField(
        max_length=10,
        choices=SUBSCRIPTION_CHOICES,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = f"scandinavian_delight_{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_code} - {self.user.username}"

    def get_total_cost(self):
        return sum(item.get_total_price() for item in self.cartitems.all())

# ---------------- Cart Items ----------------
class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True, blank=True)
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE, null=True, blank=True)
    grams = models.IntegerField(default=0)  # for ingredients
    quantity = models.IntegerField(default=0)  # for snacks
    ordered = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cartitems", null=True, blank=True)

    def __str__(self):
        if self.ingredient:
            return f"{self.ingredient.title} ({self.grams} g)"
        elif self.snack:
            return f"{self.snack.title} ({self.quantity} pcs)"
        return "Cart Item"

    def get_total_price(self):
        if self.ingredient:
            return (self.grams / 100) * self.ingredient.price_per_100g
        elif self.snack:
            return self.quantity * float(self.snack.price)
        return 0

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={'pk': self.pk})
