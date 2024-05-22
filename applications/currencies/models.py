from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.core.models import UUIDModel


class Currency(UUIDModel):
    name = models.CharField(max_length=100)
    num_code = models.CharField(max_length=3)
    sym_code = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class CurrencyRate(models.Model):
    class CurrencyType(models.TextChoices):
        SELL = "sell", _("Sell")
        BUY = "buy", _("Buy")
        CROSS = "cross", _("Cross")

    currency1 = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=False, blank=False, related_name="from_rates"
    )
    currency2 = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False, blank=False, related_name="to_rates")
    rate = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False)
    rate_type = models.CharField(max_length=5, choices=CurrencyType.choices, null=False, blank=False)
    date = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"[{self.currency1}] - [{self.currency2}]: {self.rate} | {self.rate_type} | {self.date}"
