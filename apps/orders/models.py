from apps.users import models as users_models

from django.db import models


class Order(models.Model):
    CANCELLED = 0
    CREATED = 1
    ACCEPTED = 2
    FINISHED = 3

    STATUS_CHOICES = [
        (CANCELLED, 'Cancelled'),
        (CREATED, 'Created'),
        (ACCEPTED, 'Accepted'),
        (FINISHED, 'Finished')
    ]

    client = models.ForeignKey(
        users_models.Client,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True
    )
    driver = models.ForeignKey(
        users_models.Driver,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True
    )
    status = models.PositiveSmallIntegerField(
        "Status of the order",
        choices=STATUS_CHOICES, 
        default=1
    )
    date_created = models.DateField(
        auto_now_add=True
    )
    date_updated = models.DateField(
        auto_now=True
    )

    class Meta:
        db_table = 'orders'
    
    def __str__(self) -> str:
        return f"order {self.id}"

    def get_human_readable_status_value(self) -> str:
        status = self.get_status_display()
        return status
