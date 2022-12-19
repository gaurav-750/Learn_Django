from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

router = DefaultRouter()
# *register our viewsets with router
router.register('products', viewset=views.ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
    # *products:
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),

    # *collections:
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(),
         name='collection-detail'),
]
