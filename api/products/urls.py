from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryListView, CouponListView, ProductViewSet

router = DefaultRouter()
router.register("products", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("coupons/", CouponListView.as_view(), name="coupon-list"),
]
