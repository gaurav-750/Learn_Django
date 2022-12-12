from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from django.db.models.aggregates import Count, Min, Max, Sum, Avg

from store.models import Product, Customer, Collection, Order, OrderItem
# Create your views here.
# * It take a req and returns a response
# * Request Handler


def sayHello(req):

    #! Retreive
    # try:
    #     query_set = Product.objects.all()
    #     print('query_set:', type(query_set))

    #     product1 = Product.objects.get(pk=1)
    #     print('Product 1:', product1)
    # except ObjectDoesNotExist:
    #     pass

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
    queryset = Customer.objects.filter(email__endswith='.com')

    # Collections which dont have any featured product
    collections = Collection.objects.filter(featured_product_id__isnull=True)
    # print(list(collections))

    # Product with inventory < 10
    prods = Product.objects.filter(inventory__lt=10)
    # print(list(prods))

    # Orders placed by customer with id -> 1
    ordersBy1 = Order.objects.filter(customer_id=1)
    # print(list(ordersBy1))

    # Order items for product in collection 3
    res = OrderItem.objects.filter(product__collection__id=3)
    # print(list(res))

    #! Multiple Filters:
    # Products : inventory < 10 and price < 20
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=10)
    # queryset = Product.objects.filter(
    #     inventory__lt=10).filter(unit_price__lt=20)

    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) | Q(unit_price__lt=20))

    # queryset = Product.objects.filter(inventory=F('unit_price'))

    #! Sorting
    # queryset = Product.objects.order_by('title')

    #! Limiting:
    # queryset = Product.objects.all()[0:5]

    #! Selecting fields to query
    queryset = Product.objects.values(
        'id', 'title', 'unit_price', 'collection__title')

    # ? Select products that have been ordered, sort them by title
    queryset = Product.objects.filter(
        id=F('orderitem__product_id')).distinct().order_by('title')

    # OR
    queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()
                                      ).order_by('title')

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
    res = Product.objects.filter(collection__id=3).aggregate(
        count=Count('id'), min_price=Min('unit_price'))

    # ? EXERCISE:
    # How many orders do we have?
    res = Order.objects.aggregate(Count('id'))

    # How many units of product 1 have we sold?
    res = OrderItem.objects.filter(
        product_id=1).aggregate(units_sold=Sum('quantity'))

    # How many orders had customer 1 placed?
    res = Order.objects.filter(customer_id=1).aggregate(
        customer1_totalOrders=Count('id'))

    # What is min, max and avg price of products in collection 3?
    res = Product.objects.filter(collection_id=3).aggregate(
        min_price=Min('unit_price'),
        max_price=Max('unit_price'),
        avg_price=Avg('unit_price')
    )
    print(res)

    return render(req, 'hello.html', {'name': "Gaurav", 'result': res})
