from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Coupon, Product


class CategoryAPITest(APITestCase):
    """카테고리 API 테스트"""

    def setUp(self):
        self.category1 = Category.objects.create(name="전자기기")
        self.category2 = Category.objects.create(name="의류")
        self.category3 = Category.objects.create(name="식품")

    def test_category_list(self):
        """카테고리 목록 조회 테스트"""
        url = reverse("category-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["name"], "전자기기")
        self.assertEqual(response.data[1]["name"], "의류")
        self.assertEqual(response.data[2]["name"], "식품")


class ProductAPITest(APITestCase):
    """상품 API 테스트"""

    def setUp(self):
        self.category1 = Category.objects.create(name="전자기기")
        self.category2 = Category.objects.create(name="의류")

        self.product1 = Product.objects.create(
            name="스마트폰",
            description="최신 스마트폰",
            price=1000000,
            category=self.category1,
            discount_rate=Decimal("0.1"),  # 10% 할인
            coupon_applicable=True,
        )

        self.product2 = Product.objects.create(
            name="노트북",
            description="고성능 노트북",
            price=2000000,
            category=self.category1,
            discount_rate=Decimal("0"),  # 할인 없음
            coupon_applicable=True,
        )

        self.product3 = Product.objects.create(
            name="티셔츠",
            description="면 티셔츠",
            price=30000,
            category=self.category2,
            discount_rate=Decimal("0.2"),  # 20% 할인
            coupon_applicable=False,
        )

        # 테스트 쿠폰 생성
        self.coupon = Coupon.objects.create(
            code="SAVE20", discount_rate=Decimal("0.2")  # 20% 할인
        )

    def test_product_list(self):
        """상품 목록 조회 테스트"""
        url = reverse("product-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # 정렬 순서는 created_at 역순이므로, 가장 최근에 생성된 상품이 먼저 나옴
        self.assertEqual(response.data[0]["name"], "티셔츠")
        self.assertEqual(response.data[1]["name"], "노트북")
        self.assertEqual(response.data[2]["name"], "스마트폰")

    def test_product_filter_by_category(self):
        """카테고리별 상품 필터링 테스트"""
        url = reverse("product-list")
        response = self.client.get(f"{url}?category_id={self.category1.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # 전자기기 카테고리 상품
        products = [item["name"] for item in response.data]
        self.assertIn("스마트폰", products)
        self.assertIn("노트북", products)
        self.assertNotIn("티셔츠", products)

    def test_product_detail(self):
        """상품 상세 정보 테스트"""
        url = reverse("product-detail", args=[self.product1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["name"], "스마트폰")
        self.assertEqual(response.data["price"], 1000000)
        self.assertEqual(response.data["discount_rate"], 0.1)

        # 할인된 가격 확인 (10% 할인)
        self.assertEqual(response.data["discounted_price"], 900000)

        # 쿠폰 적용 전이므로 applied_coupon은 None
        self.assertIsNone(response.data["applied_coupon"])

    def test_product_detail_with_coupon(self):
        """쿠폰이 적용된 상품 상세 정보 테스트"""
        url = reverse("product-detail", args=[self.product1.id])
        response = self.client.get(f"{url}?coupon_id={self.coupon.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["name"], "스마트폰")

        # 할인된 가격 확인 (1000000 * (1-0.1) = 900000)
        self.assertEqual(response.data["discounted_price"], 900000)

        # 쿠폰 적용 정보 확인
        self.assertIsNotNone(response.data["applied_coupon"])
        self.assertEqual(response.data["applied_coupon"]["coupon"]["code"], "SAVE20")
        # 상품 할인율 + 쿠폰 할인율 적용한 가격 (900000 * (1-0.2) = 720000)
        self.assertEqual(response.data["applied_coupon"]["discounted_price"], 720000)

    def test_coupon_not_applicable_product(self):
        """쿠폰 적용 불가능 상품 테스트"""
        url = reverse("product-detail", args=[self.product3.id])
        response = self.client.get(f"{url}?coupon_id={self.coupon.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 상품 기본 정보 확인
        self.assertEqual(response.data["name"], "티셔츠")

        # 할인된 가격 확인 (20% 할인만 적용, 쿠폰 적용 안됨)
        self.assertEqual(
            response.data["discounted_price"], 24000
        )  # 30000 * (1-0.2) = 24000

        # 쿠폰 적용 불가능하므로 applied_coupon은 None
        self.assertIsNone(response.data["applied_coupon"])


class CouponAPITest(APITestCase):
    """쿠폰 API 테스트"""

    def setUp(self):
        self.coupon1 = Coupon.objects.create(
            code="WELCOME10", discount_rate=Decimal("0.1")
        )
        self.coupon2 = Coupon.objects.create(
            code="SPECIAL50", discount_rate=Decimal("0.5")
        )

    def test_coupon_list(self):
        """쿠폰 목록 조회 테스트"""
        url = reverse("coupon-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        coupons = {item["code"]: item["discount_rate"] for item in response.data}
        self.assertEqual(coupons["WELCOME10"], 0.1)
        self.assertEqual(coupons["SPECIAL50"], 0.5)
