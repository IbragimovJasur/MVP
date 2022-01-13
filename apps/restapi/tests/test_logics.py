from apps.orders.models import Order
from apps.users.models import Client, Driver, User

from rest_framework.authtoken.models import Token


def create_user_instance(username: str, phone: str, password: str) -> User:
    """Function creates a user instance"""
    user = User.objects.create_user(
            username=username, phone=phone, password=password)
    return user


def authenticate_user(client, user: User) -> None:
    """Function authenticates user using his/her token"""
    token = str(Token.objects.get(user=user))
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)


def create_driver_instance(user: User) -> Driver:
    """Function create a driver model instance"""
    driver = Driver.objects.create(user=user)
    return driver


def create_order_instance(client: Client, driver: Driver) -> Order:
    """Function create a order model instance"""
    order = Order.objects.create(client=client, driver=driver)
    return order
