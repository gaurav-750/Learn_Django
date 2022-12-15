from django.contrib import admin
from store.admin import ProductAdmin
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline

from store.models import Product

# Register your models here.


class TagInline(GenericTabularInline):
    model = TaggedItem

    autocomplete_fields = ['tag']
    min_num = 1
    max_num = 5
    extra = 0


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
