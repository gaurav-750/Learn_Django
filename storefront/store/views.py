from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .models import Product
from .serializers import ProductSerializer

# Create your views here.


@api_view()
def product_list(req):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(req, id):

    product = get_object_or_404(Product, pk=id)

    # this serializer will convert our product object to a dictionary
    # and we get that through serializer.data
    serializer = ProductSerializer(product)
    return Response(serializer.data)
