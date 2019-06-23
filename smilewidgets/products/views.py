from rest_framework import generics

from .models import ProductPrice


class ProductPriceList(generics.ListCreateAPIView):
    queryset = ProductPrice
    

