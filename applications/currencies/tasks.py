import logging

from iso.iso4217 import Currencies as ISOCurrencies

from applications.currencies.models import Currency, CurrencyRate
from applications.currencies.services import MonobankAPIService
from currency.celery import app as celery_app


@celery_app.task
def fetch_currency_data():
    data = MonobankAPIService(logger=logging.getLogger(__name__)).get_currencies()
    for currency_data in data:
        currency1 = get_or_create_currency.delay(currency_data["code1"])
        currency2 = get_or_create_currency.delay(currency_data["code2"])

        if not currency1 or not currency2:
            logging.error("Failed to get or create currency")
            continue

        currency, _ = CurrencyRate.objects.get_or_create(
            currency1=currency1,
            currency2=currency2,
            rate=currency_data["rate"],
            rate_type=currency_data["rate_type"],
            date=currency_data["date"],
        )


@celery_app.task
def get_or_create_currency(currency_code: str):
    currency = Currency.objects.get(num_code=currency_code)
    if not currency:
        currency = create_currency.delay(currency_code)
    return currency


@celery_app.task
def create_currency(currency_code: str):
    currency = ISOCurrencies.search_by(num=currency_code)
    if currency:
        currency = Currency.objects.create(
            name=currency.currency,
            num_code=currency_code,
            sym_code=currency.code,
        )
        logging.info(f"Currency created: {currency}")
        return currency
    else:
        logging.error(f"Failed to create currency with code: {currency_code}")
