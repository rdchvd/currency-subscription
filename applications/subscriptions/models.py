from django.contrib.auth.models import User, AbstractUser
from django.db import models

from applications.currencies.models import Currency
from applications.core.models import UUIDModel


class UUIDUser(UUIDModel, AbstractUser):
    ...


class CurrencySubscription(UUIDModel):
    user = models.ForeignKey(UUIDUser, on_delete=models.CASCADE, related_name="currency_subscriptions")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="subscriptions")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.currency}"
