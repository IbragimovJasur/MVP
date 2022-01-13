from apps.orders.models import Order
from apps.users.models import Client

from rest_framework.permissions import BasePermission


class IsCurrentOrderOwner(BasePermission):
    """Checking whether requesting user is owner of order"""
    def has_permission(self, request, view):
        try:
            order = Order.objects.get(pk=view.kwargs.get('pk_order'))
            return order.client.user == request.user
        except Order.DoesNotExist:
            #in case object doesn't exist nobody gets a permission
            return False


class IsCurrentClientUser(BasePermission):
    """Checking whether requesting user is user in client instance"""
    def has_permission(self, request, view):
        try:
            client = Client.objects.get(pk=view.kwargs.get('pk_client'))
            return client.user == request.user
        except Client.DoesNotExist:
            #if object doesn't or user isn't client user
            #user won't get a permission
            return False
