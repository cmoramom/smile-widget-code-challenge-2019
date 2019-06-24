from datetime import date
from calendar import calendar

from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProductPrice


class ProductPriceGetPrice(APIView):
    # def get(self, request, format=None):
    #     # queryset = [ProductPrice.objects.all()]
    #     # serializer_class = ProductPriceSerializer
    #     #
    #     # return Response(queryset)
    parser_classes = (JSONParser,)
    black_friday_date = settings.BLACK_FRIDAY['Dates']

    def post(self, request, format=None):

        try:
            product_code = request.data['productCode']
        except KeyError as e:
            return Response({"error": "Product code missing "})

        try:
            promo_date = request.data['date']
        except KeyError as e:
            return Response({"error": "Promo Date missing "})
        try:
            gift_card = request.data['giftCardCode']
        except KeyError:
            gift_card = 0

        # if the promo_date sent by the user is black friday date, it will query for the promo_date but with the
        # isBlack_friday set to true
        # isBlack_friday set to true

        if promo_date[5::] in self.black_friday_date:

            price = ProductPrice.objects.filter(code_id=product_code, promo_date_start=promo_date,
                                                isBlack_friday=True).first()
        else:
            # if the promo date sent by the user is not a black friday it  means that we need to check if there is
            # a price that starts in the 2019 but with isBlack_friday set to false

            start_date = f"{date.today().year}-{date.today().month - (12 - date.today().month)+1}-01"
            end_date = f"{date.today().year}-{date.today().month + (12 - date.today().month)}-31"

            price = ProductPrice.objects.filter(code_id=product_code, promo_date_start__range=[start_date, end_date],
                                                isBlack_friday=False).first()

        if price is not None:
            return Response({"Price": f"${price.price}"})
        return Response({"Error": "No data found for the specific date and promo code"})
