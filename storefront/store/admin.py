from django.contrib import admin

from . import models

# This class defines how we want to view/edit our Products


class ProductAdmin(admin.ModelAdmin):
    # this fields will be displayed on Product page
    list_display = ['id', 'title', 'unit_price']

    # specify the fields which can be edited:
    list_editable = ['unit_price']

    # 20 products will be displayed per page
    list_per_page = 20


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_per_page = 50

    list_editable = ['membership']
    ordering = ['first_name', 'last_name']


# * Register your models here.
admin.site.register(models.Collection)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Customer, CustomerAdmin)
