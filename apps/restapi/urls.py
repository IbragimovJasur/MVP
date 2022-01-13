import apps.restapi.views as restapi_views

from django.urls import path


app_name = 'restapi'
urlpatterns = [
    #orders
    path('orders/create/', restapi_views.OrderCreateView.as_view(),
          name='order_create'),
    path('orders/<int:pk_order>/update-status/', 
          restapi_views.OrderUpdateView.as_view(),
          name='order_update'),
    path('orders/<int:pk_order>/clients/<int:pk_client>/', 
          restapi_views.ClientOrderListView.as_view(),
          name='client_order_list')
]
