import logging

import requests


class MonobankAPIService:
    URL = "https://api.monobank.ua/bank/currency"

    def __init__(self, logger):
        self.logger = logger or logging.getLogger(__name__)

    def get_currencies_request_data(self):
        response = requests.get(self.URL)
        if not response.ok:
            self.logger.error(f"Failed to get currencies data: {response.text}")
            return
        return response.json()

    @staticmethod
    def _get_rate_type_dict(data, currency_dict, rate_key, rate_name):
        if rate := data.get(rate_key):
            return {
                **currency_dict,
                "rate_type": rate_name,
                "rate": rate,
            }

    @classmethod
    def _format_currency_data(cls, currencies):
        formatted_currencies = []
        for currency in currencies:
            currency_dict = {
                "code1": currency["currencyCodeA"],
                "code2": currency["currencyCodeB"],
                "date": currency["date"],
            }
            buy_rate = cls._get_rate_type_dict(currency, currency_dict, "rateBuy", "buy")
            sell_rate = cls._get_rate_type_dict(currency, currency_dict, "rateSell", "sell")
            cross_rate = cls._get_rate_type_dict(currency, currency_dict, "rateCross", "cross")

            formatted_currencies.extend(filter(None, [buy_rate, sell_rate, cross_rate]))
        return formatted_currencies

    def get_currencies(self):
        data = self.get_currencies_request_data()
        data = self._format_currency_data(data)
        return data
