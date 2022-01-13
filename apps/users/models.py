from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    """Customized child of AbstractUser class"""
    first_name = models.CharField(
        "First Name", max_length=250, null=True, blank=True
    )
    last_name = models.CharField(
        "Last Name", max_length=250, null=True, blank=True
    )
    phone = models.CharField(
        "Phone", max_length=13, unique=True
    )
    email = models.EmailField(
        "Email", null=True, blank=True
    )
    
    class Meta:
        db_table = 'users'

    def __str__(self) -> str:
        return self.username


class Driver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        related_name='driver', 
        on_delete=models.CASCADE
    )
    car_name = models.CharField(
        "Name of driver's car", max_length=250, null=True, blank=True
    )
    #TODO: add extra fields (ranking,) and new relations (Car,)

    class Meta:
        db_table = 'drivers'

    def __str__(self) -> str:
        return self.user.username
    

class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        related_name='client', 
        on_delete=models.CASCADE
    )
    #TODO: add extra fields (location,) and new relations (Balance,)

    class Meta:
        db_table = 'clients'

    def __str__(self) -> str:
        return self.user.username
