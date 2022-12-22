from django.db import models
from datetime import datetime

from django.core.validators import MinValueValidator
from uuid import uuid4
from django.conf import settings
from django.contrib import admin
# Create your models here


class Collection(models.Model):
    title = models.CharField(max_length=255)

    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    # products


class Product(models.Model):
    # define the fields of this Class
    title = models.CharField(max_length=255)  # varchar(255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    # *1-many : 1 collection can contain many Products
    collection = models.ForeignKey(
        "Collection", on_delete=models.PROTECT)

    #! Many-Many rel:
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.title + ", $" + str(self.unit_price)

    class Meta:
        ordering = ['id']
        # verbose_name = 'Product'


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # If we want more control on our Database, we'd use the Meta class

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name


class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_COMPLETED = 'C'
    STATUS_FAILED = 'F'
    STATUS = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
    ]

    # when we create order, django will automatically fill this field
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=STATUS, default='P')

    # *1-many : 1 customer can have many Orders:
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT)


class OrderItem(models.Model):
    # *1-many
    order = models.ForeignKey("Order", on_delete=models.PROTECT)
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # *1-1
    # customer = models.OneToOneField(
    # "Customer", on_delete=models.CASCADE, primary_key=True)

    # *1-many
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # in cart, we'll have a field called cartitem_set => we can override it by related_name = ''
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
