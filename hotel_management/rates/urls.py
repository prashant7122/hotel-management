from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomRateViewSet,
    OverriddenRoomRateViewSet,
    DiscountViewSet,
    DiscountRoomRateViewSet,
    get_lowest_rate, map_room_rates_to_discounts,
)


router = DefaultRouter()
router.register(r'room-rates', RoomRateViewSet)
router.register(r'overridden-room-rates', OverriddenRoomRateViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'discount-room-rates', DiscountRoomRateViewSet)

urlpatterns = [
    # Include API views from router
    path('', include(router.urls)),
    # Add endpoint for lowest rate
    path('lowest-rate/<int:room_id>/<str:start_date>/<str:end_date>/', get_lowest_rate),

    path('map-room-rates-to-discounts/', map_room_rates_to_discounts, name='map-room-rates-to-discounts'),


]
