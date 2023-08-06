import requests

from exchange_escuela_it.bases.base_exchange_converter import BaseExchangeConverter


class EURCoverter(BaseExchangeConverter):
    currency_code = "EUR"
    url = f"https://api.exchangeratesapi.io/latest?base={currency_code}"

    def get_values_from_api(self):
        response = requests.get(self.url)
        return response.json().get("rates")
