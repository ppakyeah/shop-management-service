from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from .models import Category, Coupon, Product
from .serializers import (CategorySerializer, CouponSerializer,
                          ProductDetailSerializer, ProductListSerializer)


class CategoryListView(generics.ListAPIView):
    """
    카테고리 목록 API
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    상품 조회 API
    """

    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category_id"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        coupon_id = self.request.query_params.get("coupon_id")
        if coupon_id:
            try:
                coupon = Coupon.objects.get(id=coupon_id)
                context["coupon"] = coupon
            except Coupon.DoesNotExist:
                pass

        return context

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="coupon_id",
                description="적용할 쿠폰 ID",
                type=OpenApiTypes.INT,
                required=False,
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        """상품 상세 조회 및 선택적 쿠폰 적용"""
        return super().retrieve(request, *args, **kwargs)


class CouponListView(generics.ListAPIView):
    """
    쿠폰 목록 API
    """

    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
