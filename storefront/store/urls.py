from django.urls import path
from . import views

urlpatterns = [
    # *products:
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),

    # *collections:
    path('collections/', views.collection_list),
    path('collections/<int:pk>/', views.collection_detail,
         name='collection-detail'),
]
