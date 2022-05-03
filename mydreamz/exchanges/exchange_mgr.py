
from mydreamz.exchanges.exchange import exchange

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
        return self.exchange_count

    def get_exchange_details(self):
        return self.exchange
