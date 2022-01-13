import apps.restapi.serializers as restapi_serializers
import apps.restapi.permissions as restapi_permissions
from apps.restapi import business_logics
from apps.orders.models import Order

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class OrderCreateView(generics.CreateAPIView):
    """View is for creating new order"""
    permission_classes = (IsAuthenticated,)
    serializer_class = restapi_serializers.OrderSerializer

    def perform_create(self, serializer):
        client = self.request.user.client
        serializer.save(client=client)


class OrderUpdateView(generics.UpdateAPIView):
    """View is for updating status of an order"""
    permission_classes = (IsAuthenticated, 
                          restapi_permissions.IsCurrentOrderOwner)
    serializer_class = restapi_serializers.OrderUpdateSerializer

    def update(self, request, *args, **kwargs):
        try:
            input_status = int(request.data['status'])
            order = Order.objects.get(pk=kwargs.get('pk_order'))

            if business_logics.check_status_change_not_allowed(order, input_status):
                return Response(
                    data={'message':'Accepted order cannot be cancelled'},
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            
            serializer = self.get_serializer(order, data=request.data)
            updated_instance = business_logics.update_order_instance(
                                                   self, serializer)
            return updated_instance

        except:
            return Response(
                       data={'message':"Order object doesn't exist"},
                       status=status.HTTP_404_NOT_FOUND)


class ClientOrderListView(generics.ListAPIView):
    """View is for getting all orders done by a particular client"""
    permission_classes = (IsAuthenticated, 
                          restapi_permissions.IsCurrentClientUser)
    serializer_class = restapi_serializers.OrderListSerializer
    
    def get_queryset(self):
        search_query_params = self.request.query_params
        client = self.kwargs.get('pk_client')
        if search_query_params:
            date_from = self.request.query_params.get('from')
            date_to = self.request.query_params.get('to')

            if None in (date_from, date_to):
                #didn't handle exceptions in case date values are wrong
                #assuming requests will be using calendar, not through endpoint
                raise Exception("Arguments 'from' or 'to' cannot be empty")

            filtered_orders = business_logics.filter_orders_using_dates(
                                date_from, date_to, client)
            return filtered_orders

        all_client_orders = business_logics.get_all_orders_by_client(client)
        return all_client_orders

    def get(self, *args, **kwargs):
        try:
           orders=self.get_serializer(self.get_queryset(),many=True).data
           return Response(orders, status=status.HTTP_200_OK)

        except Exception as error:
            context = {"error": str(error)}
            return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)
