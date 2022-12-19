from django.urls import path
from . import views
from django.urls import path, include
from rest_framework_nested import routers


router = routers.DefaultRouter()
# *register our viewsets with router
router.register('products', viewset=views.ProductViewSet)
router.register('collections', viewset=views.CollectionViewSet)

# Child routers:
products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')


urlpatterns = [
    # *routers
    path("", include(router.urls)),
    path("", include(products_router.urls)),

    # *products:
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),

    # *collections:
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>/', views.CollectionDetail.as_view(),
    #      name='collection-detail'),
]
