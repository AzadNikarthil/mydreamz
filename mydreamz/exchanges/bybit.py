from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.base_exchange import BaseExchange

class ByBit(BaseExchange):
    """
    """

    def __init__(self, service_store):
        """
        """
        BaseExchange.__init__(self, service_store)

    def get_coin_pair(self):
        """
        """
        new_pair = ['BTC/USD:BTC']
        return new_pair

    def get_fiat_currency_name(self, pair): 
        cur = pair.split("/")[1]
        currency = cur.split(":")[0]
        if currency == "USDC":
            return "USD"
        elif currency == "USDT":
            return "USD"
        elif currency == "UST":
            return "USD"
        elif currency == "BUSD":
            return "USD"
        elif currency == "DAI":
            return "USD"
        elif currency == "TUSD":
            return "USD"
        elif currency == "MIM":
            return "USD"
        else:
            return currency






