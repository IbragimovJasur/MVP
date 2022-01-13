from apps.orders.models import Order
from apps.users.models import Driver

from rest_framework import serializers


class DriverSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Driver
        fields = ['user', 'car_name']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ['client', 'status', 'date_created', 'date_updated']


class OrderUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        exclude = ['client', 'driver', 'date_created', 'date_updated']


class OrderListSerializer(serializers.ModelSerializer):
    order_status = serializers.ReadOnlyField(
                        source='get_human_readable_status_value')
    driver = serializers.SerializerMethodField(
                method_name='get_info_about_driver')

    class Meta:
        model = Order
        fields = ['id', 'driver', 'order_status', 'date_updated']
    
    def get_info_about_driver(self, obj):
        driver = obj.driver
        return DriverSerializer(driver).data
