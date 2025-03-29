from django.urls import include, path

from api.products import urls as products_urls

urlpatterns = [path("", include(products_urls))]
