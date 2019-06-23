from abc import ABC

from rest_framework import serializers
from .models import ProductPrice


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('price')
    #
    # pk = serializers.IntegerField(read_only=True)
    # code = serializers.IntegerField(read_only=True)
    # price = serializers.IntegerField(read_only=True)
    # promo_date_start = serializers.DateField(read_only=True)
    # isActive = serializers.BooleanField(read_only=True)
