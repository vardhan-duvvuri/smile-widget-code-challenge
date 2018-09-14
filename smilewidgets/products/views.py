from django.shortcuts import render
from django.db.models.query import Q

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import serializers

from .models import GiftCard, Product, ProductPrice


class PriceQuerySerializer(serializers.Serializer):
    """Serializer to validate get-price API params."""
    date = serializers.DateField()
    productCode = serializers.CharField(max_length=10)
    giftCardCode = serializers.CharField(max_length=30, required=False)


@api_view()
def get_price(request):
    """API view to get the price on given date based on giftCardCode."""
    params = PriceQuerySerializer(data=request.query_params)
    params.is_valid(True)

    date = params.data['date']
    product_code = params.data['productCode']
    gift_card_code = params.data.get('giftCardCode', None)

    try:
        product = Product.objects.get(code=product_code)
    except Product.DoesNotExist:
        raise APIException(f"{product_code!r}: No such product exists.")

    if gift_card_code:
        try:
            gift_card = GiftCard.objects.get(code=gift_card_code)
        except GiftCard.DoesNotExist:
            raise APIException(f"{gift_card_code!r}: No such gift card exists.")
    else:
        gift_card = None

    q = Q(date_start__lte=date) & (
        Q(date_end__isnull=True) | Q(date_end__gte=date))
    product_price = product.productprice_set.filter(q).first()

    price = (product_price or product).price
    if gift_card:
        price = max(0, price - gift_card.amount)

    return Response({
        'price': price,
    })
