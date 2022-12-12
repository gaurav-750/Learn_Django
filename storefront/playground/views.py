from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

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

    # return HttpResponse("Hello World!")
    return render(req, 'hello.html', {'name': "Gaurav", 'customers': list(queryset)})
