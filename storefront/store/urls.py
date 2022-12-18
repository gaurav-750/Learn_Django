from django.urls import path
from . import views

urlpatterns = [
    # *products:
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetail.as_view()),

    # *collections:
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.collection_detail,
         name='collection-detail'),
]
