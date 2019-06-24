from datetime import date


from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import ProductPrice, GiftCard


class ProductPriceGetPrice(APIView):




    def post(self, request, format=None):

        # using Post to retrieve date since post is more safer because it is not stored in server logs, and browser
        # history and we are sending sensitive data like producCode and Giftcard number, also if this app is deployed
        # in a https domain, the post request will be encrypted
        # but the get request always will send the param in the url


        # https: // security.stackexchange.com / questions / 33837 / get - vs - post - which - is -more - secure

        parser_classes = (JSONParser,)
        black_friday_date = settings.BLACK_FRIDAY['Dates']

        try:
            product_code = request.data['productCode']
        except KeyError as e:
            return Response({"error": "Product code missing "},status=200)

        try:
            promo_date = request.data['date']
        except KeyError as e:
            return Response({"error": "Promo Date missing "},status=200)
        try:
            gift_card = request.data['giftCardCode']
        except KeyError:
            gift_card = 0

        # if the promo_date sent by the user is black friday date, it will query for the promo_date but with the
        # isBlack_friday set to true
        # isBlack_friday set to true

        if promo_date[5::] in black_friday_date:

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

            gift_card = GiftCard.objects.filter(code=gift_card, date_start__lt=date.today(),
                                                ).first() # date_end__gte=date.today()

            final_price = price.price

            if gift_card is not None:
                discount = gift_card.amount/100
                if discount <= 100:
                    final_price = (price.price-(discount/100)*price.price)

            return Response({"Price": f"${final_price}"}, status=200)
        return Response({"Error": "No data found for the specific date and promo code"})
