from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Category, Coupon, Product


class CategorySerializer(serializers.ModelSerializer):
    """카테고리"""

    class Meta:
        model = Category
        fields = ["id", "name"]


class CouponSerializer(serializers.ModelSerializer):
    """쿠폰"""

    discount_rate = serializers.FloatField()

    class Meta:
        model = Coupon
        fields = ["id", "code", "discount_rate"]


class ProductCouponSerializer(serializers.Serializer):
    """상품 쿠폰 적용 정보"""

    coupon = CouponSerializer(read_only=True)
    discounted_price = serializers.IntegerField(
        help_text="쿠폰 할인율 적용한 최종 가격"
    )


class ProductListSerializer(serializers.ModelSerializer):
    """상품 목록 정보"""

    category = CategorySerializer(read_only=True)
    discount_rate = serializers.FloatField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "discount_rate",
            "coupon_applicable",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """상품 상세 정보"""

    category = CategorySerializer(read_only=True)
    discount_rate = serializers.FloatField()
    discounted_price = serializers.SerializerMethodField(
        help_text="상품 할인율 적용 가격"
    )
    applied_coupon = serializers.SerializerMethodField(
        allow_null=True, help_text="적용된 쿠폰 정보"
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "discount_rate",
            "coupon_applicable",
            "discounted_price",
            "applied_coupon",
        ]

    @extend_schema_field(OpenApiTypes.INT)
    def get_discounted_price(self, obj):
        """할인된 가격 반환"""
        return int(obj.price * (1 - float(obj.discount_rate)))

    @extend_schema_field(ProductCouponSerializer)
    def get_applied_coupon(self, obj):
        """적용된 쿠폰 정보 반환"""
        coupon = self.context.get("coupon")

        if coupon and obj.coupon_applicable:
            discounted_price = int(
                self.get_discounted_price(obj) * (1 - float(coupon.discount_rate))
            )
            return ProductCouponSerializer(
                {"coupon": coupon, "discounted_price": discounted_price}
            ).data
        return None
