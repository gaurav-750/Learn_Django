from django.urls import path
from . import views
from django.urls import path, include
from rest_framework_nested import routers


router = routers.DefaultRouter()
# *register our viewsets with router
router.register('products', viewset=views.ProductViewSet, basename='products')
router.register('collections', viewset=views.CollectionViewSet)
router.register('carts', viewset=views.CartViewSet)

# Child routers:
# products/1/reviews/1
products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

# carts/1/cartitems/1
carts_router = routers.NestedDefaultRouter(
    router, 'carts', lookup='cart')
carts_router.register('cartitems', views.CartItemViewSet,
                      basename='cart-cartitems')

urlpatterns = [
    # *routers
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    path("", include(carts_router.urls)),

    # *products:
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),

    # *collections:
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>/', views.CollectionDetail.as_view(),
    #      name='collection-detail'),
]
