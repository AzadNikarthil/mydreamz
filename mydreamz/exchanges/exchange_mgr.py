
from mydreamz.exchanges.exchange import exchange
from mydreamz.exchanges.base_exchange import BaseExchange 

from mydreamz.exchanges.coinbase import CoinBase
class ExchangeMgr:
    """
    """

    def __init__(self, service_store):
        """
        """
        self.exchange = exchange
        self.exchange_count = len(self.exchange.keys())
        self.service_store = service_store

    def get_exchange_count(self):
        """
        """
        return self.exchange_count

    def get_exchange_details(self):
        """
        """
        return self.exchange

    def get_exchange_obj(self, exchange_name):
        """
        """
        exchange = None
        if exchange_name == "coinbase":
            exchange = CoinBase(self.service_store)
        else:
            exchange = BaseExchange(self.service_store)
        exchange.set_exchange_name(exchange_name)

        return exchange

