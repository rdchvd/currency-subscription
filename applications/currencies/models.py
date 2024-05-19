from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.core.models import UUIDModel


class Currency(UUIDModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class CurrencyRate(models.Model):
    class CurrencyType(models.TextChoices):
        SELL = "sell", _("Sell")
        BUY = "buy", _("Buy")

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="rates", null=False, blank=False)
    rate = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False)
    rate_type = models.CharField(max_length=5, choices=CurrencyType.choices, null=False, blank=False)
    date = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"[{self.date}][{self.rate_type}]: {self.currency} - {self.rate}"
