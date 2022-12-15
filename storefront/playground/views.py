from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField,  CharField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Min, Max, Sum, Avg
from django.contrib.contenttypes.models import ContentType

from store.models import Product, Customer, Collection, Order, OrderItem, Cart, CartItem
from tags.models import TaggedItem

from datetime import datetime
# Create your views here.
# *It take a req and returns a response
# *Request Handler


def sayHello(req):

    #! Retreive
    try:
        queryset = Product.objects.all()
        print('query_set:', type(queryset))
        print(queryset)

    #     product1 = Product.objects.get(pk=1)
    #     print('Product 1:', product1)
    except ObjectDoesNotExist:
        pass

    #! Filter
    # prods = Product.objects.filter(unit_price__gt=20)
    # queryset = Product.objects.filter(unit_price__range=(20, 30))

    # *getting products which have collection id -> 3
    # queryset = Product.objects.filter(collection__id=3)

    # *getting products in which title contains 'coffee'
    # queryset = Product.objects.filter(title__icontains='coffee')
    # products = list(queryset)

    # ? EXERCISE:
    # Customers with .com accounts:
    # queryset = Customer.objects.filter(email__endswith='.com')

    # Collections which dont have any featured product
    # collections = Collection.objects.filter(featured_product_id__isnull=True)
    # print(list(collections))

    # Product with inventory < 10
    # prods = Product.objects.filter(inventory__lt=10)
    # print(list(prods))

    # Orders placed by customer with id -> 1
    # ordersBy1 = Order.objects.filter(customer_id=1)
    # print(list(ordersBy1))

    # Order items for product in collection 3
    # res = OrderItem.objects.filter(product__collection__id=3)
    # print(list(res))

    #! Multiple Filters:
    # Products : inventory < 10 and price < 20
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=10)
    # queryset = Product.objects.filter(
    #     inventory__lt=10).filter(unit_price__lt=20)

    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) | Q(unit_price__lt=20))

    # queryset = Product.objects.filter(inventory=F('unit_price'))

    # queryset = Product.objects.order_by('title').filter(inventory__lte=10)

    #! Sorting
    # queryset = Product.objects.order_by('title')

    #! Limiting:
    # queryset = Product.objects.all()[0:5]

    #! Selecting fields to query
    # queryset = Product.objects.values(
    #     'id', 'title', 'unit_price', 'collection__title')

    # ? Select products that have been ordered, sort them by title
    # queryset = Product.objects.filter(
    #     id=F('orderitem__product_id')).distinct().order_by('title')

    # OR
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()
    #   ).order_by('title')

    # *only()
    # queryset = Product.objects.only('id', 'title', 'unit_price')[0:5]
    # print(list(queryset))

    # queryset = Product.objects.defer('description')[0:5]
    # print(list(queryset))

    #! Selecting related objects:
    # queryset = Product.objects.select_related('collection').all()[0:5]

    # queryset = Product.objects.prefetch_related(
    #     'promotions').select_related('collection').all()

    # queryset = Order.objects.select_related(
    #     'customer').order_by('-placed_at')[:5]
    # print(list(queryset))

    #! Aggregation
    # queryset = Product.objects.filter(collection__id=3).aggregate(
    #     count=Count('id'), min_price=Min('unit_price'))

    # ? EXERCISE:
    # How many orders do we have?
    # res = Order.objects.aggregate(Count('id'))

    # How many units of product 1 have we sold?
    # res = OrderItem.objects.filter(
    #     product_id=1).aggregate(units_sold=Sum('quantity'))

    # How many orders had customer 1 placed?
    # queryset = Order.objects.filter(customer_id=1).aggregate(
    #     customer1_totalOrders=Count('id'))

    # What is min, max and avg price of products in collection 3?
    # res = Product.objects.filter(collection_id=3).aggregate(
    #     min_price=Min('unit_price'),
    #     max_price=Max('unit_price'),
    #     avg_price=Avg('unit_price')
    # )
    # print(res)

    #! Annotate
    # res = Customer.objects.annotate(isNew=Value(True))
    # res = Customer.objects.annotate(new_id=F('id')+1)
    # res = Customer.objects.annotate(total_customers=Value(
    #     Customer.objects.aggregate(Count('id'))['id__count']))

    #! DB Functions:
    # res = Customer.objects.annotate(
    #     fullName=Func(F('first_name'), Value(" "), F('last_name'), function='CONCAT'))
    # OR
    # res = Customer.objects.annotate(
    # fullName=Concat('first_name', Value(' '), 'last_name')
    # )

    #! Grouping
    # Find the total orders each Customer has placed:
    # res = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    #! Working with complex expressions (somewhat)
    # discount = ExpressionWrapper(
    #     F('unit_price')*0.9, output_field=DecimalField())
    # res = Product.objects.annotate(
    #     discounted_price=discount).defer('description')

    # res = Product.objects.annotate(
    #     dis_price=ExpressionWrapper(
    #         F('unit_price') * 0.70, output_field=DecimalField())
    # )

    # ? EXERCISE:
    # Find customers along with their last order id:
    # res = Customer.objects.annotate(
    #     last_order_id=Max('order__id')
    # )

    # 'Collections' and their count of products
    # res = Collection.objects.annotate(
    # total_products=Count('product__collection_id')
    # )

    # Customers with > 5 orders:
    # res = Customer.objects.annotate(
    #     total_orders=Count('order__customer_id')
    # ).filter(total_orders__gt=5)

    # Customers and the total amount they've spent:
    # res = Customer.objects.annotate(
    #     amount_spent=Sum(
    #         F('order__orderitem__quantity') *
    #         F('order__orderitem__unit_price')
    #     )
    # )

    # Top 5 best selling products and their total sales:
    # res = Product.objects.annotate(
    #     total_sales=Sum(
    #         F('orderitem__unit_price') *
    #         F('orderitem__quantity')
    #     )).order_by('-total_sales')[0:5]

    #! Querying Generic Relationships:
    # We need to find the tags for a particular product
    # 1. Find the content_type_id from ContentType Table
    # content_type = ContentType.objects.get_for_model(Product)

    # queryset = TaggedItem.objects \
    #     .select_related('tag') \
    #     .filter(
    #         content_type=content_type,
    #         object_id=1
    #     )

    # queryset = Product.objects.all()
    # queryset[0]
    # list(queryset)

    #! Creating objects -> Insert
    # collection = Collection()
    # collection.title = 'Video Games'
    # # collection.featured_product_id = 1
    # collection.featured_product = Product(pk=1)
    # collection.save()

    # Collection.objects.create(title='Sports', featured_product=Product(id=2))
    # Collection.objects.create(title='Accessories', featured_product_id=10)

    #! Updating objects
    # coll = Collection(pk=11)
    # print('coll:', coll)
    # coll.title = 'Video Games'
    # coll.featured_product = Product(pk=1)
    # coll.save()
    # * Its not the right way to update as it causes data loss

    # coll = Collection.objects.get(pk=11)
    # print('coll:', coll)
    # coll.title = 'Games'
    # coll.featured_product = None
    # coll.save()

    # todo (OR)
    # Collection.objects.filter(pk=11).update(featured_product_id=None)

    #! Deleting objects:
    # Collection.objects.filter(pk__gt=10).delete()

    # todo EXERCISE:
    # Create a shopping cart with an item:
    # cart = Cart()
    # cart.created_at = datetime.now()
    # cart.save()

    # CartItem.objects.create(quantity=2, cart_id=1,
    # product=Product.objects.get(pk=1))

    # Update the quantity of an item in a shopping cart
    # CartItem.objects.filter(pk=1).update(quantity=3)

    # Remove a shopping cart with its items
    # Cart.objects.filter(pk=1).delete()

    #! Transactions
    # with transaction.atomic():
    #     new_order = Order()
    #     new_order.customer_id = 1
    #     new_order.id = 1001
    #     new_order.save()

    #     item = OrderItem()
    #     item.order = new_order
    #     item.product_id = 1
    #     item.quantity = 10
    #     item.unit_price = 20
    #     item.save()

    #! Raw SQL queries:
    # queryset = Order.objects.raw(
    #     "delete from store_order where id = 1004"
    # )

    # print('qs:', queryset)

    with connection.cursor() as cursor:
        res = cursor.execute(
            "select * from store_collection limit 10")
        print('res=', res)
        records = cursor.fetchall()
        print(records)
        print(records[0])

    return render(req, 'hello.html', {'name': "Gaurav", "result": res})
