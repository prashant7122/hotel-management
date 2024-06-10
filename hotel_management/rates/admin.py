from django.contrib import admin
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate


@admin.register(RoomRate)
class RoomRateAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'room_name', 'default_rate']
    search_fields = ['room_name']
    list_filter = ['default_rate']


@admin.register(OverriddenRoomRate)
class OverriddenRoomRateAdmin(admin.ModelAdmin):
    list_display = ['room_rate', 'overridden_rate', 'stay_date']
    search_fields = ['room_rate__room_name']
    list_filter = ['stay_date']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discount_id', 'discount_name', 'discount_type', 'discount_value']
    search_fields = ['discount_name']
    list_filter = ['discount_type']


@admin.register(DiscountRoomRate)
class DiscountRoomRateAdmin(admin.ModelAdmin):
    list_display = ['room_rate', 'discount']
    search_fields = ['room_rate__room_name', 'discount__discount_name']
