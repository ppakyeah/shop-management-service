from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from api.products.models import Category, Coupon, Product


class Command(BaseCommand):
    help = "초기 카테고리, 상품, 쿠폰 데이터를 생성합니다."

    @transaction.atomic
    def handle(self, *args, **options):
        # 데이터 존재 여부 확인
        if (
            Category.objects.exists()
            or Product.objects.exists()
            or Coupon.objects.exists()
        ):
            return

        # 기존 데이터 삭제
        Coupon.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        # 카테고리 생성
        category_names = ["의류", "가전제품", "식품", "가구", "도서"]

        for name in category_names:
            Category.objects.create(name=name)

        # 카테고리 다시 가져오기
        categories = list(Category.objects.all())

        self.stdout.write(self.style.SUCCESS(f"카테고리 {len(categories)}개 생성 완료"))

        # 상품 생성
        products = [
            # 의류
            Product(
                name="여름용 티셔츠",
                description="시원한 여름용 티셔츠입니다.",
                price=25000,
                category=categories[0],
                discount_rate=Decimal("0.10"),
                coupon_applicable=True,
            ),
            Product(
                name="청바지",
                description="편안한 스트레치 청바지입니다.",
                price=55000,
                category=categories[0],
                discount_rate=Decimal("0.05"),
                coupon_applicable=True,
            ),
            # 가전제품
            Product(
                name="스마트 TV",
                description="4K 해상도의 스마트 TV입니다.",
                price=750000,
                category=categories[1],
                discount_rate=Decimal("0.15"),
                coupon_applicable=False,
            ),
            Product(
                name="노트북",
                description="고성능 노트북입니다.",
                price=1200000,
                category=categories[1],
                discount_rate=Decimal("0.08"),
                coupon_applicable=True,
            ),
            # 식품
            Product(
                name="과일 세트",
                description="신선한 제철 과일 세트입니다.",
                price=35000,
                category=categories[2],
                discount_rate=Decimal("0.0"),
                coupon_applicable=True,
            ),
            # 가구
            Product(
                name="책상",
                description="원목 책상입니다.",
                price=150000,
                category=categories[3],
                discount_rate=Decimal("0.20"),
                coupon_applicable=False,
            ),
            # 도서
            Product(
                name="프로그래밍 책",
                description="초보자를 위한 프로그래밍 입문서입니다.",
                price=28000,
                category=categories[4],
                discount_rate=Decimal("0.0"),
                coupon_applicable=True,
            ),
        ]
        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS(f"상품 {len(products)}개 생성 완료"))

        # 쿠폰 생성
        coupons = [
            Coupon(code="WELCOME10", discount_rate=Decimal("0.10")),
            Coupon(code="SUMMER20", discount_rate=Decimal("0.20")),
            Coupon(code="SPECIAL30", discount_rate=Decimal("0.30")),
        ]
        Coupon.objects.bulk_create(coupons)
        self.stdout.write(self.style.SUCCESS(f"쿠폰 {len(coupons)}개 생성 완료"))

        self.stdout.write(self.style.SUCCESS("모든 초기 데이터 생성 완료!"))
