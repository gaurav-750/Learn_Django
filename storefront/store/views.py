from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    CreateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, \
    IsAuthenticatedOrReadOnly, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Collection, Review, Cart, CartItem, Customer
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, \
    CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, \
    CustomerSerializer
from .filters import ProductFilter
from .pagination import CustomPagination

from .permissions import IsAdminOrReadOnly

# Create your views here.

# *Creating a ViewSet for Products


class ProductViewSet(ModelViewSet):
    # *Filtering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']

    # We can also Custom filter class:
    filterset_class = ProductFilter

    # searching:
    search_fields = ['title', 'description']

    # sort:
    ordering_fields = ['unit_price', 'last_update']

    # *Pagination -> We can also set it globally in SETTINGS -> REST_FRAMEWORK
    # pagination_class = PageNumberPagination
    pagination_class = CustomPagination

    # !set the custom permission class
    permission_classes = [IsAdminOrReadOnly]

    # *List, Post, Retreive, Update are handled here
    # queryset = Product.objects.all()
    def get_queryset(self):
        queryset = Product.objects.all()
        # collection_id = self.request.query_params.get('collection_id')

        # if collection_id is not None:
        #     queryset = queryset.filter(collection_id=collection_id)
        return queryset

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

    permission_classes = [IsAdminOrReadOnly]

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


# todo 'Reviews':
class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    def get_queryset(self):
        # print('self.kwargs => ', self.kwargs)
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


# todo 'Cart'
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):

    queryset = Cart.objects.prefetch_related('cartitems').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    # *allowed http methods
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        # {'cart_pk': 'd3b07bdcf1de41419148b5f7b41e10b2'}
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')

    def get_serializer_class(self):  # POST
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':  # PATCH
            return UpdateCartItemSerializer
        else:  # GET, DELETE
            return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class CustomerViewSet(ModelViewSet):
    # POST
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # *Setting the permission:
    # todo Will only allow permission if user is 'Admin'
    permission_classes = [IsAdminUser]

    # if we want to have diff.permissions for diff.actions =>
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticated()]

    # /customers/me
    @action(detail=False, methods=['GET', 'PUT'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        # todo retrieve the customer and return it
        # request.user -> of not logged in => AnonymousUser
        # {"id": request.user.id}
        (customer, created) = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        else:  # PUT
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
