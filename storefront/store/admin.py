from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


# * Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='product_cnt')
    def products_count(self, collection):
        # reverse(admin:app_model_page)
        url = (
            reverse('admin:store_product_changelist')
            + "?"
            + urlencode({
                'collection_id': str(collection.id)
            })
        )
        print('url =>', url)
        return format_html('<a href="{}"> {} </a>', url, collection.product_cnt)

    # * Here, we r overriding the base Queryset
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_cnt=Count('product__collection_id')
        )


# todo Add a Custom Filter for inventory status:
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(
                inventory__lt=10
            )


class ProductAdmin(admin.ModelAdmin):
    # * This class defines how we want to view/edit our Products Page
    # this fields will be displayed on Product page
    list_display = ['id', 'title', 'unit_price',
                    'inventory_status', 'collection']

    # specify the fields which can be edited:
    list_editable = ['unit_price']

    # 20 products will be displayed per page
    list_per_page = 20

    # filter:
    list_filter = ['collection', 'last_update', InventoryFilter]

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        print('product:', product)
        if product.inventory < 10:
            return 'Low'
        else:
            return 'OK'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_per_page = 50
    list_editable = ['membership']

    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + "?"
            + urlencode({
                'customer_id': customer.id,
            })
        )
        print('url', url)
        return format_html('<a href="{}"> {} </a>', url, 'Orders')


# todo EXERCISE - Set up the Orders page along with their Customers
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_status', 'customer']
    ordering = ['id']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Customer, CustomerAdmin)
