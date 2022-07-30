from django.shortcuts import render
from .models import Product, Comment
from .serializer import ProductSerializer
from rest_framework import generics
from helpers.pagination import CustomPagination

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from paycomuz.views import MerchantAPIView
from paycomuz import Paycom


class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        return self.ORDER_FOUND


def successfully_payment(self, account, transaction, *args, **kwargs):
    print(account)


def cancel_payment(self, account, transaction, *args, **kwargs):
    print(account)


class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder


# Create your views here.
class AllProductView(generics.ListAPIView):
    queryset = Product.objects.select_related("category").prefetch_related("saveds", "option_value", "comments",
                                                                           "images")
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
