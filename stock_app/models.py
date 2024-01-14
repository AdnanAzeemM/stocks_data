from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import process_transaction
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.username


class StockData(models.Model):
    ticker = models.CharField(max_length=20)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.PositiveIntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.ticker


class Transaction(models.Model):
    transaction_choice = (
        ('buy', 'Buy'),
        ('sell', 'Sell')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_user')
    ticker = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=4, choices=transaction_choice)
    transaction_volume = models.PositiveIntegerField()
    transaction_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker} - {self.transaction_type}"


@receiver(post_save, sender=Transaction)
def on_transaction_created(sender, instance, created, **kwargs):
    if created:
        process_transaction.delay(instance.id)
