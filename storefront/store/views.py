from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count

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


@api_view(['GET', 'POST'])
def collection_list(req):
    if req.method == 'GET':
        # add the field 'products_count' in the collections queryset
        queryset = Collection.objects.annotate(
            products_count=Count('product')
        ).order_by('id')

        # serialize
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif req.method == 'POST':
        serializer = CollectionSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(req, pk):
    # get the required collection
    collection = Collection.objects.annotate(
        products_count=Count('product')
    ).get(pk=pk)

    if req.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif req.method == 'PUT':
        serializer = CollectionSerializer(collection, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif req.method == 'DELETE':
        # *first we need to check if this collection has any products:
        # collection.product_set.all()
        if collection.product_set.all().count() > 0:
            return Response({"error": "collection cannot be deleted because it is associated with products"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        collection.delete()
        return Response({"message": "collection deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)
