from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.


@api_view(['GET', 'POST'])
def product_list(req):

    if req.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True)

        return Response(serializer.data)
    elif req.method == 'POST':
        # This is where DeSerialization happens:
        serializer = ProductSerializer(data=req.data)

        # Data Validation -> If data is inappropriate, raise exception
        serializer.is_valid(raise_exception=True)

        # save to database:
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(req, id):
    product = get_object_or_404(Product, pk=id)

    if req.method == 'GET':
        # this serializer will convert our product object to a dictionary
        # and we get that through serializer.data
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif req.method == 'PUT':
        # deserialize -> validate -> save
        serializer = ProductSerializer(product, data=req.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)
    elif req.method == 'DELETE':
        # print(product.orderitem_set.all())
        # *check if there are any orderitems associated with this product:
        if product.orderitem_set.count() > 0:
            return Response({'error': "Product cannot be deleted because it is associated with an order item."},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(req, pk):
    queryset = Collection.objects.get(pk=pk)
    serializer = CollectionSerializer(queryset)

    return Response(serializer.data)
