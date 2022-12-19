from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models import Count

# Create your views here.

# *Creating a ViewSet for Products


class ProductViewSet(ModelViewSet):
    # *List, Post, Retreive, Update are handled here
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    # *We r overriding destroy method => as to give our own implementation
    # if we don't override, ModelViewSet will handle Delete as well
    def destroy(self, req, pk):
        product = get_object_or_404(Product, pk=pk)

        # check if product has any orderitem
        # product.orderitem.all() -> List of all orderitems
        if product.orderitem_set.all().count() > 0:
            return Response({'error': 'Cannot delete product as it is associated with some order items'})
        product.delete()
        return Response({'message': 'product deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT)


#! This is using Generic Views
# class ProductList(ListCreateAPIView):

    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    # def get_serializer_context(self):
    # return {'request': self.request}

    # (OR)
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # def get_serializer_class(self):
    #     return ProductSerializer

# class ProductDetail(RetrieveUpdateDestroyAPIView):
    # Get and Put are handled here
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    # def delete(self, req, pk):
    #     product = get_object_or_404(Product, pk=pk)

    #     # check if product has any orderitem
    #     # product.orderitem.all() -> List of all orderitems
    #     if product.orderitem_set.all().count() > 0:
    #         return Response({'error': 'Cannot delete product as it is associated with some order items'})
    #     product.delete()
    #     return Response({'message': 'product deleted successfully'},
    #                     status=status.HTTP_204_NO_CONTENT)

# *Collections Viewset
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('product')
    ).order_by('id')
    serializer_class = CollectionSerializer

    def destroy(self, req, pk):
        collection = Collection.objects.get(pk=pk)
        # *first we need to check if this collection has any products:
        # collection.product_set.all()
        if collection.product_set.all().count() > 0:
            return Response({"error": "collection cannot be deleted because it is associated with products"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        collection.delete()
        return Response({"message": "collection deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


# class CollectionList(ListCreateAPIView):

#     queryset = Collection.objects.annotate(
#         products_count=Count('product')
#     ).order_by('id')
#     serializer_class = CollectionSerializer


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     # Get and Put are handled here:
#     queryset = Collection.objects.annotate(
#         products_count=Count('product')
#     )
#     serializer_class = CollectionSerializer

#     def delete(self, req, pk):
#         collection = Collection.objects.get(pk=pk)
#         # *first we need to check if this collection has any products:
#         # collection.product_set.all()
#         if collection.product_set.all().count() > 0:
#             return Response({"error": "collection cannot be deleted because it is associated with products"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)

#         collection.delete()
#         return Response({"message": "collection deleted successfully"},
#                         status=status.HTTP_204_NO_CONTENT)


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


# *Reviews:
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
