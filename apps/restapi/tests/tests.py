from apps.users.models import Client

from decouple import config
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from . import test_logics


class OrderCreateUpdateTestCase(APITestCase):
    """
    TestCase tests order creating, updating to allowed status, 
    updating to not allowed status, and getting list of orders ordered by client
    """
    def setUp(self):
        self.user = test_logics.create_user_instance(
                        username='user', phone='11', 
                        password=config('USER1_PASSWORD'))
        #creating new user because self.user is a requesting user
        self.user2 = test_logics.create_user_instance(
                        username='user2', phone='22', 
                        password=config('USER2_PASSWORD'))

    def test_create_order(self):
        test_logics.authenticate_user(self.client, self.user)
        driver = test_logics.create_driver_instance(self.user2)
        
        url = reverse('restapi:order_create')
        data = {'driver': driver.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['driver'], driver.id)

    def test_update_order_with_allowed_status(self):
        test_logics.authenticate_user(self.client, self.user)
        client = Client.objects.get(user=self.user)
        driver = test_logics.create_driver_instance(self.user2)
        order = test_logics.create_order_instance(client, driver)

        url = reverse('restapi:order_update', kwargs={'pk_order': order.id})
        data = {'status': 3} #status: Finished
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)
        self.assertEqual(response.data['status'], 3)
    
    def test_update_order_with_notallowed_status(self):
        test_logics.authenticate_user(self.client, self.user)
        client = Client.objects.get(user=self.user)
        driver = test_logics.create_driver_instance(self.user2)
        order = test_logics.create_order_instance(client, driver)

        #changing status from Created to Accepted
        order.status = order.ACCEPTED 
        order.save()

        url = reverse('restapi:order_update', kwargs={'pk_order': order.id})
        data = {'status': 0} #status: Cancelled
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
                response.data['message'], "Accepted order cannot be cancelled")

    def test_list_client_orders(self):
        test_logics.authenticate_user(self.client, self.user)
        client = Client.objects.get(user=self.user)
        driver = test_logics.create_driver_instance(self.user2)
        order = test_logics.create_order_instance(client, driver)

        url = reverse('restapi:client_order_list', 
                kwargs={'pk_order': order.id, 'pk_client':client.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], order.id)
        self.assertEqual(response.data[0]['order_status'], 'Created')
