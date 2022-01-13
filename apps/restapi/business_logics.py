from apps.orders.models import Order
from apps.users.models import Client

from datetime import datetime

from rest_framework.response import Response


def check_status_change_not_allowed(order: Order, input_status: int) -> bool:
    """Function checks current/input status of an order"""
    if order.status == order.ACCEPTED and input_status == order.CANCELLED:
        return True


def update_order_instance(self, serializer) -> Response:
    """Function updates the order instance"""
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)


def convert_string_to_date_format(date: str) -> datetime:
    """Function converts string to datetime required format"""
    return datetime.strptime(date, '%Y-%d-%m').strftime('%Y-%m-%d')


def filter_orders_using_dates(date_from: str, date_to: str, client: Client) -> Order:
    """Function filters client orders based on given range (date_from, date_to)"""
    date_from = convert_string_to_date_format(date_from)
    date_to = convert_string_to_date_format(date_to)
    filtered_orders = Order.objects.filter(
                          date_created__range=[date_from, date_to],
                          client=client)
    return filtered_orders


def get_all_orders_by_client(pk_client: int) -> Order:
    """Function returns all orders ordered by client"""
    client = Client.objects.get(pk=pk_client)
    orders = Order.objects.filter(client=client)
    return orders
