from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count

# Create your views here.

# *Class Based Views:


#! This is using Generic Views
class ProductList(ListCreateAPIView):

    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    # (OR)
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


# class ProductList(APIView):
#     def get(self, req):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             queryset, many=True)
#         return Response(serializer.data)

#     def post(self, req):
#         # This is where DeSerialization happens:
#         serializer = ProductSerializer(data=req.data)

#         # Data Validation -> If data is inappropriate, raise exception
#         serializer.is_valid(raise_exception=True)
#         # save to database:
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # *Here we have some logic, hence we 'override' the delete method:
    def delete(self, req, pk):
        product = get_object_or_404(Product, pk=pk)

        # print(product.orderitem_set.all())
        # *check if there are any orderitems associated with this product:
        if product.orderitem_set.count() > 0:
            return Response({'error': "Product cannot be deleted because it is associated with an order item."},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get(self, req, id):
    #     product = get_object_or_404(Product, pk=id)
    #     # this serializer will convert our product object to a dictionary
    #     # and we get that through serializer.data
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)

    # def put(self, req, id):
    #     product = get_object_or_404(Product, pk=id)

    #     # deserialize -> validate -> save
    #     serializer = ProductSerializer(product, data=req.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


class CollectionList(ListCreateAPIView):

    queryset = Collection.objects.annotate(
        products_count=Count('product')
    ).order_by('id')
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    # Get and Put are handled here:
    queryset = Collection.objects.annotate(
        products_count=Count('product')
    )
    serializer_class = CollectionSerializer

    def delete(self, req, pk):
        collection = Collection.objects.get(pk=pk)
        # *first we need to check if this collection has any products:
        # collection.product_set.all()
        if collection.product_set.all().count() > 0:
            return Response({"error": "collection cannot be deleted because it is associated with products"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        collection.delete()
        return Response({"message": "collection deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def collection_list(req):
#     if req.method == 'GET':
#         # add the field 'products_count' in the collections queryset
#         queryset = Collection.objects.annotate(
#             products_count=Count('product')
#         ).order_by('id')

#         # serialize
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif req.method == 'POST':
#         serializer = CollectionSerializer(data=req.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'POST'])
# def product_list(req):
#     if req.method == 'GET':

#     elif req.method == 'POST':


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(req, id):
#     product = get_object_or_404(Product, pk=id)

#     if req.method == 'GET':

#     elif req.method == 'PUT':

#     elif req.method == 'DELETE':
