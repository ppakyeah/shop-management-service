from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="카테고리명")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="상품명")
    description = models.TextField(verbose_name="상품 설명")
    price = models.PositiveIntegerField(verbose_name="가격(원)")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="카테고리",
    )
    discount_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name="할인율"
    )
    coupon_applicable = models.BooleanField(
        default=False, verbose_name="쿠폰 적용 가능 여부"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["-created_at"]


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="쿠폰 코드")
    discount_rate = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="할인율"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    def __str__(self):
        return f"{self.code} ({self.discount_rate * 100}% 할인)"

    class Meta:
        verbose_name = "coupon"
        verbose_name_plural = "coupons"
