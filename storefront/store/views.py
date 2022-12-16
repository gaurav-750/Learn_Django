from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


@api_view()
def product_list(req):
    print('req:', req)
    return Response('ok')


@api_view()
def product_detail(req, id):
    print('req', req, id)
    return Response({
        "message": "OK",
        "id": id,
    })
