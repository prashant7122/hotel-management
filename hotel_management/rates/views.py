import pandas as pd
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate
from .serializers import (
    RoomRateSerializer,
    OverriddenRoomRateSerializer,
    DiscountSerializer,
    DiscountRoomRateSerializer, RoomRateDiscountMappingSerializer,
)


class RoomRateViewSet(viewsets.ModelViewSet):
    queryset = RoomRate.objects.all()
    serializer_class = RoomRateSerializer


class OverriddenRoomRateViewSet(viewsets.ModelViewSet):
    queryset = OverriddenRoomRate.objects.all()
    serializer_class = OverriddenRoomRateSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class DiscountRoomRateViewSet(viewsets.ModelViewSet):
    queryset = DiscountRoomRate.objects.all()
    serializer_class = DiscountRoomRateSerializer


@api_view(['GET'])
def get_lowest_rate(request, room_id, start_date, end_date):
    try:
        room_rate = RoomRate.objects.get(room_id=room_id)
    except RoomRate.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)

    overridden_rates = OverriddenRoomRate.objects.filter(
        room_rate=room_rate, stay_date__range=[start_date, end_date]
    )
    discounts = DiscountRoomRate.objects.filter(room_rate=room_rate)

    rates = {}
    for overridden_rate in overridden_rates:
        rates[overridden_rate.stay_date.strftime('%Y-%m-%d')] = overridden_rate.overridden_rate

    for date in pd.date_range(start=start_date, end=end_date):
        date_str = date.strftime('%Y-%m-%d')
        if date_str not in rates:
            rates[date_str] = room_rate.default_rate

    final_rates = {}
    for date, rate in rates.items():
        highest_discount = 0
        for discount_rate in discounts:
            discount = discount_rate.discount
            if discount.discount_type == 'fixed':
                highest_discount = max(highest_discount, discount.discount_value)
            else:  # percentage
                highest_discount = max(highest_discount, rate * (discount.discount_value / 100))

        final_rates[date] = rate - highest_discount

    return Response(final_rates)


@api_view(['POST'])
def map_room_rates_to_discounts(request):
    serializer = RoomRateDiscountMappingSerializer(data=request.data)
    if serializer.is_valid():
        room_rate_ids = serializer.validated_data['room_rate_ids']
        discount_ids = serializer.validated_data['discount_ids']

        room_rates = RoomRate.objects.filter(id__in=room_rate_ids)
        discounts = Discount.objects.filter(id__in=discount_ids)

        for room_rate in room_rates:
            for discount in discounts:
                DiscountRoomRate.objects.get_or_create(room_rate=room_rate, discount=discount)

        return Response({"message": "Room rates and discounts mapped successfully."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)